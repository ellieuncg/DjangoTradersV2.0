# recommender.py (new file)
from django.db.models import Count, F, Q, Value, IntegerField
from django.db.models.functions import ExtractMonth, ExtractYear
from collections import defaultdict
from typing import List, Dict, Tuple
from .models import Product, OrderDetail, Customer


class ProductRecommender:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id

    def get_recommendations(self, limit: int = 5) -> List[Dict]:
        """
        Get product recommendations for a customer based on various factors.
        Returns list of recommended products with scores and reasons.
        """
        frequently_bought = self._get_frequently_bought_products()
        category_based = self._get_category_based_recommendations()
        similar_customers = self._get_similar_customer_recommendations()

        all_recommendations = self._combine_recommendations(
            frequently_bought, category_based, similar_customers
        )

        sorted_recommendations = sorted(
            all_recommendations.items(), key=lambda x: x[1]["score"], reverse=True
        )

        recommended_products = []
        for product_id, details in sorted_recommendations[:limit]:
            try:
                product = Product.objects.get(product_id=product_id)
                recommended_products.append(
                    {
                        "product": product,
                        "score": details["score"],
                        "reasons": details["reasons"],
                    }
                )
            except Product.DoesNotExist:
                continue

        return recommended_products

    def _get_frequently_bought_products(self) -> Dict:
        """Get products the customer frequently buys."""
        frequently_bought = (
            OrderDetail.objects.filter(order__customer_id=self.customer_id)
            .values("product")
            .annotate(purchase_count=Count("order_detail_id"))
            .order_by("-purchase_count")
        )

        return {
            item["product"]: {
                "score": item["purchase_count"] * 2,
                "reason": "Previously purchased",
            }
            for item in frequently_bought
        }

    def _get_category_based_recommendations(self) -> Dict:
        """Get recommendations based on categories the customer likes."""
        favorite_categories = (
            OrderDetail.objects.filter(order__customer_id=self.customer_id)
            .values("product__category")
            .annotate(category_count=Count("order_detail_id"))
            .order_by("-category_count")
        )

        recommendations = {}
        for category in favorite_categories:
            similar_products = (
                Product.objects.filter(
                    category_id=category["product__category"], status="active"
                )
                .exclude(orderdetails__order__customer_id=self.customer_id)
                .annotate(
                    category_score=Value(
                        category["category_count"], output_field=IntegerField()
                    )
                )
            )

            for product in similar_products:
                recommendations[product.product_id] = {
                    "score": category["category_count"],
                    "reason": f"Similar to products you like",
                }

        return recommendations

    def _get_similar_customer_recommendations(self) -> Dict:
        """Get recommendations based on similar customers' purchases."""
        customer_categories = (
            OrderDetail.objects.filter(order__customer_id=self.customer_id)
            .values_list("product__category", flat=True)
            .distinct()
        )

        similar_customers = (
            OrderDetail.objects.filter(product__category__in=customer_categories)
            .exclude(order__customer_id=self.customer_id)
            .values("order__customer")
            .annotate(common_categories=Count("product__category", distinct=True))
            .filter(common_categories__gte=len(customer_categories) * 0.5)
            .values_list("order__customer_id", flat=True)
        )

        similar_purchases = (
            OrderDetail.objects.filter(order__customer_id__in=similar_customers)
            .exclude(product__orderdetails__order__customer_id=self.customer_id)
            .values("product")
            .annotate(purchase_count=Count("order_detail_id"))
        )

        return {
            item["product"]: {
                "score": item["purchase_count"],
                "reason": "Popular with similar customers",
            }
            for item in similar_purchases
        }

    def _combine_recommendations(self, *recommendation_sets) -> Dict:
        """Combine different recommendation sets with weights."""
        combined = defaultdict(lambda: {"score": 0, "reasons": set()})

        for recommendations in recommendation_sets:
            for product_id, details in recommendations.items():
                combined[product_id]["score"] += details["score"]
                combined[product_id]["reasons"].add(details["reason"])

        return {
            k: {"score": v["score"], "reasons": list(v["reasons"])}
            for k, v in combined.items()
        }
