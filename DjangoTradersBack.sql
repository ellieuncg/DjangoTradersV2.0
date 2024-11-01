PGDMP      0                |           DjangoTraders    16.4    16.4 .               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16400    DjangoTraders    DATABASE     �   CREATE DATABASE "DjangoTraders" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE "DjangoTraders";
                postgres    false            �            1259    16402 
   categories    TABLE     �   CREATE TABLE public.categories (
    category_id integer NOT NULL,
    category_name character varying(255),
    description character varying(255)
);
    DROP TABLE public.categories;
       public         heap    postgres    false            �            1259    16401    categories_category_id_seq    SEQUENCE     �   CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.categories_category_id_seq;
       public          postgres    false    216                       0    0    categories_category_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;
          public          postgres    false    215            �            1259    16412 	   customers    TABLE     (  CREATE TABLE public.customers (
    customer_id integer NOT NULL,
    customer_name character varying(255),
    contact_name character varying(255),
    address character varying(255),
    city character varying(255),
    postal_code character varying(255),
    country character varying(255)
);
    DROP TABLE public.customers;
       public         heap    postgres    false            �            1259    16411    customers_customer_id_seq    SEQUENCE     �   CREATE SEQUENCE public.customers_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.customers_customer_id_seq;
       public          postgres    false    218                       0    0    customers_customer_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.customers_customer_id_seq OWNED BY public.customers.customer_id;
          public          postgres    false    217            �            1259    16439    order_details    TABLE     �   CREATE TABLE public.order_details (
    order_detail_id integer NOT NULL,
    order_id integer,
    product_id integer,
    quantity integer
);
 !   DROP TABLE public.order_details;
       public         heap    postgres    false            �            1259    16438 !   order_details_order_detail_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_details_order_detail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.order_details_order_detail_id_seq;
       public          postgres    false    224                       0    0 !   order_details_order_detail_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.order_details_order_detail_id_seq OWNED BY public.order_details.order_detail_id;
          public          postgres    false    223            �            1259    16432    orders    TABLE     l   CREATE TABLE public.orders (
    order_id integer NOT NULL,
    customer_id integer,
    order_date date
);
    DROP TABLE public.orders;
       public         heap    postgres    false            �            1259    16431    orders_order_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.orders_order_id_seq;
       public          postgres    false    222                       0    0    orders_order_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;
          public          postgres    false    221            �            1259    16423    products    TABLE     �   CREATE TABLE public.products (
    product_id integer NOT NULL,
    product_name character varying(255),
    category_id integer,
    unit character varying(255),
    price numeric(10,2)
);
    DROP TABLE public.products;
       public         heap    postgres    false            �            1259    16422    products_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.products_product_id_seq;
       public          postgres    false    220                        0    0    products_product_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;
          public          postgres    false    219            �            1259    16446    testproducts    TABLE     �   CREATE TABLE public.testproducts (
    testproduct_id integer NOT NULL,
    product_name character varying(255),
    category_id integer
);
     DROP TABLE public.testproducts;
       public         heap    postgres    false            �            1259    16445    testproducts_testproduct_id_seq    SEQUENCE     �   CREATE SEQUENCE public.testproducts_testproduct_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.testproducts_testproduct_id_seq;
       public          postgres    false    226            !           0    0    testproducts_testproduct_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.testproducts_testproduct_id_seq OWNED BY public.testproducts.testproduct_id;
          public          postgres    false    225            i           2604    16405    categories category_id    DEFAULT     �   ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);
 E   ALTER TABLE public.categories ALTER COLUMN category_id DROP DEFAULT;
       public          postgres    false    215    216    216            j           2604    16415    customers customer_id    DEFAULT     ~   ALTER TABLE ONLY public.customers ALTER COLUMN customer_id SET DEFAULT nextval('public.customers_customer_id_seq'::regclass);
 D   ALTER TABLE public.customers ALTER COLUMN customer_id DROP DEFAULT;
       public          postgres    false    217    218    218            m           2604    16442    order_details order_detail_id    DEFAULT     �   ALTER TABLE ONLY public.order_details ALTER COLUMN order_detail_id SET DEFAULT nextval('public.order_details_order_detail_id_seq'::regclass);
 L   ALTER TABLE public.order_details ALTER COLUMN order_detail_id DROP DEFAULT;
       public          postgres    false    223    224    224            l           2604    16435    orders order_id    DEFAULT     r   ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);
 >   ALTER TABLE public.orders ALTER COLUMN order_id DROP DEFAULT;
       public          postgres    false    222    221    222            k           2604    16426    products product_id    DEFAULT     z   ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);
 B   ALTER TABLE public.products ALTER COLUMN product_id DROP DEFAULT;
       public          postgres    false    220    219    220            n           2604    16449    testproducts testproduct_id    DEFAULT     �   ALTER TABLE ONLY public.testproducts ALTER COLUMN testproduct_id SET DEFAULT nextval('public.testproducts_testproduct_id_seq'::regclass);
 J   ALTER TABLE public.testproducts ALTER COLUMN testproduct_id DROP DEFAULT;
       public          postgres    false    225    226    226                      0    16402 
   categories 
   TABLE DATA           M   COPY public.categories (category_id, category_name, description) FROM stdin;
    public          postgres    false    216   [4                 0    16412 	   customers 
   TABLE DATA           r   COPY public.customers (customer_id, customer_name, contact_name, address, city, postal_code, country) FROM stdin;
    public          postgres    false    218   ]5                 0    16439    order_details 
   TABLE DATA           X   COPY public.order_details (order_detail_id, order_id, product_id, quantity) FROM stdin;
    public          postgres    false    224   �E                 0    16432    orders 
   TABLE DATA           C   COPY public.orders (order_id, customer_id, order_date) FROM stdin;
    public          postgres    false    222   �y                 0    16423    products 
   TABLE DATA           V   COPY public.products (product_id, product_name, category_id, unit, price) FROM stdin;
    public          postgres    false    220   u�                 0    16446    testproducts 
   TABLE DATA           Q   COPY public.testproducts (testproduct_id, product_name, category_id) FROM stdin;
    public          postgres    false    226   w�       "           0    0    categories_category_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.categories_category_id_seq', 8, true);
          public          postgres    false    215            #           0    0    customers_customer_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.customers_customer_id_seq', 91, true);
          public          postgres    false    217            $           0    0 !   order_details_order_detail_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.order_details_order_detail_id_seq', 2155, true);
          public          postgres    false    223            %           0    0    orders_order_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.orders_order_id_seq', 1, false);
          public          postgres    false    221            &           0    0    products_product_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.products_product_id_seq', 1, false);
          public          postgres    false    219            '           0    0    testproducts_testproduct_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.testproducts_testproduct_id_seq', 10, true);
          public          postgres    false    225            p           2606    16409    categories categories_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);
 D   ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_pkey;
       public            postgres    false    216            r           2606    16419    customers customers_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);
 B   ALTER TABLE ONLY public.customers DROP CONSTRAINT customers_pkey;
       public            postgres    false    218            x           2606    16444     order_details order_details_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_pkey PRIMARY KEY (order_detail_id);
 J   ALTER TABLE ONLY public.order_details DROP CONSTRAINT order_details_pkey;
       public            postgres    false    224            v           2606    16437    orders orders_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public            postgres    false    222            t           2606    16430    products products_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public            postgres    false    220            z           2606    16451    testproducts testproducts_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.testproducts
    ADD CONSTRAINT testproducts_pkey PRIMARY KEY (testproduct_id);
 H   ALTER TABLE ONLY public.testproducts DROP CONSTRAINT testproducts_pkey;
       public            postgres    false    226               �   x^-�Kn�0D��)|��A��ֱ��
ȶZ%B� ��})%����P���Ns̡t�c�Ȧs9@��wX%���;�������PZO���auu�1G9�L�'A�SL'���	p%�$f��Ty�źب�?5�}3E�9�թzV�j��|3�$�:9�9<%��4�I�ӵ!�a~@e;�u.|7#c!��Z����3p�j�5>�@�s+{�e�����Q��i?�����Z�)�y            x^}��r"I������1۫BC	�%�C��$F�[�c{$!�&ɠ� <ѾǾ�~	�z{lں�%J��W���kaW�����[WVVݛ�=�W�(���V/��B�C5�E�ru��������VW�s����w�e^_���3�ʗ��76����#j��2zeuf���e�:u>�]�Q���K�����P��ӍN��z�R��y}��{�l��ma���\�2<<���E=�w>��ƅ��6V�E��7~gJ������U��l�\���W>W/�HG�s��]+���3�(u���r��^M7ut��������ͮm�5�3kԢ=����ve��@M2�}��Z}i3�5�-K�+����=u��=⿦!���ƺ�$���%t*�im���>[�W��f�bG���U��?U��M�3�Z}�Yz�h�)��.�j0�t:���m%j�3��4l�Vi_Xm�R�}���v�0��t�e��@qU���&�nO-���g����jfj:ɧ���mL^R�o��W��_�A!PZ�eU��t��3E�*�k_�,3��綶*�����,m��3��>�U���K�n��z���.����{���������HM�tK��ږ�W�V>E�y�E�QצΫ��d���WӮ��@ojҪ.?KF�4�x3����p�^/�n_���-
Wy���Ԥޥ��O�:�s\ U+��yUx�zʝ:�����zg�ʸ���RεZ8��[����h4:��琝ǤQ��߷��r���-���������*��K-3��p�Ż�����W�(V`D��A����jnW<���a��?���fu�?ߘS�0^�M�yf���;}�P���Zрy#�c"V�j�r�����I��sy���x��楎�zR�w[����3҃YӠ��,˗Y]�i�Vj�N�*sv�^LV��ݮ5l4oQq�3���(Q�����iis����^�̲�s�4}{��?j�W�O{�oJ����h���{.$�۴�"ẜ'}�^��(���p|ޯ��/r�nG]���\����G�����ݬe4נ�*	@��3-.zmv.���d+Z'S0-�z��~�c����ڼ>��1�M�����b����K����ga�t���\\�/ԥ�k��<O�@�&;��h �d��Dz����k M�a+��81��O�Y*J`7>���(���̍S��%��K��}9n�}�ѯ��䤃3�G�s���D���l��0x��ǝ������(y"p�e��œ|��<3�Q���:`J:I'�T����4�_A�&�~�0�E�ٹ�R1��|��m����栍��{)��x4z��И��DV�ǏA>}���>�NG�V&C�a�Z:?1�ɨ��ܩ��aҥ����׵=j�_��N�N���/t�ˏ!-FE�a��<A�6 +��|Q, 	��~��ժ�(Ҙ7Ĩ'�[���V �&p���E����"�Ae������T��������A|�G�ᡰ��'!,��U�:��G��|T�Q�!�I9}N_�ԬP�k��r���/E��}!�ݞ�-U���!0>���)��ö���{�2H���߹�^��Zu�=�*N�uU#V���NO���x������l6n?��B?��s��;
���7{�g�cn2�9��UtUd&�ԯ�~䍦�G�D �-h)��Ә�I)��_�(/�=�����Ʊ�~;?�>>��K:���\y���<�Q^(P\,Җ7�{������ţ�%�^�@�b�<��0�ݯ�>P��|�O�������b���7_23F*�W�c0v3�G��h@3��T(��;&LR(��|��{��Y�~p�ME1}*F��LUzg1m*�?�F� �Y�d�V�ۂ���Dݖ����R�����aPx3�e0D�P��N9�j�8�>�{����F�w��`U}��|��y���ޛzi� ޣ��T=_�Ӌ�Czu6�����v��f��:�D���3���g�%0N^_Յ�[� �	��j�|��~$�L9u\:+Zz��1ĕ����;ڞy|ta
���AHv���;��'ka�t��zv�Zq�����wp�� {�h����
�Ր���w��w���A�3s<�;}G2��Pi"_Z�	O�r2k@�Y��� �K�O��tZ�}5��	+"�qQx�9>.�<�e�R��.�޾֠�\�_h5�İ�Ggb�P�����^`ԠZ���\�<2���ԋ���Y���j�5X�Ԍ�l/jB��5��y(o|��~����LJ�����(�3���b텉�
%OTy
V��Q�C>��-�&�h��^���=�.�C�},��7�<���y�"���
v%��g� ��s��'����LT<��5hR
\�)@tH&�)�b�BeFMS���&��	�\�;d���7����,kttV���W'~���$�}!��?�4�px��K�)�ld�噛Ѩ���:F-&E���`�vq󉅘�]+�p��e�+��mKf��{a�M֪�>ꓩ��M�M�� �$a+�7�$�n}Y�%�?�,p2��
G�(W�Y�?�5"?wqO=HP�;�M\"�p�3�����s���S���O�x���_!f��cʵ�-ҩJ�<�X!�����^�n�������7��u'1�(iH�=���*��c��/�n�@��)#K�aS�Z"˔��
����HTd��x�H�/�Y�H��y���_1�!���M!_�j���X��J?�>aY4�d>f��d��-�"���4�=$̕$@�ި��$�S���)~L}��4ü��!�c�v8�/��K���! A����H��f�ӊGj�0��MY��&���tcOo�+3a="'i��)�� ���S�ԖĆ�<��_]��e�j�o������i7����u'�<;�!��p��H���΄|�S xwc�ܽR���F�������Q{0���~�2�:6�E狇y�6Cnp��~e�0T�d�����a[�p2�����/�ӻ��>�������i�#���ަ�w��U%���Xg�^���k,�M]A�<29�9�@��|�G���"bs(���ʅy�`�Elh��DCv�;��Xֲ��?$�F�8�d�k���N>߉k)ܱY��<J�S���:P)Z��䝲}�Ȫ��O��4����R�9���A��O�'��1��cjC���:I�$r�F�c��"��^B-�dKq���J��� �xc����7�i�um��7)��)+-٥
��N�0�	Iebڙ��L��S�Q���SZ��@���^�Ȯd�km�V����aBQ�r,s$�s��Ck(�|�m��|u^��Ⓛ`ؼa�p���UL�,�`�jIo���C�{4̓�A#^�,P�;�U�u�M�M-�9>mY�ź�0�g����z�x2�?�A%[˝���"�Z���2zol��|{isiKk(k��ԫӮF]R�<lD�CȔ���d�\J��E��9��ȯ�=̢������p
XZ���2ݼ[�����#����1�B|�`�tY5(�S��` d���l)!v���?�j��QBﲂt���X�)YdK�_#V�w3w��gc�~��W
�(�#N.��'�£%������A5�HL�c&��ف�᪥u�%[�H��G��nuo��bUt�N�'����(�]�'�Z�|�,�d/�K	Y|�uD\�5��]�2 ͯ�ǊD/�e��)O�ݐ�R��;&�l���*���|�����O�!���\Zz��{��+�C\�:dC[%�I�d�7[9�˃YԐ�{i@s�Nq�ݶ�I0KQ��f�3��&�<H�]� ,vf]f~�$�c�H(i �<I?��&���� <݊� 	;�Su^��b$��]�d�_�2vAP�R�'XC�d����6Vǳ����d��ri�v�R�p����3�!KԻz�Be���9s�}�ߎ�umЦEވ�vbT��@΋�B�d�������t��U�q�ەZ��묆����]Ry�����Z�!��N�!�������4�q���a��c��"����i }   ~�t�U��C��d����c��6�輯Y�s\o���P����L}gH��⫂W�|�`�l���pQ� �J��]��󲸏����Zʣݪ:��׈5���&�v���G⥔�/Z�����Y            x^M�Y�c�����yV,�{���������dW�3��@"}������?������wН?.��^?��]����>��������=~�{���u�~�=.{��=w��ۇ�??������ny\`������r���o�do���],��g�J�q���ك1����.�(�~F���t���C��H�{����_�`0V���who���E��s{B��	���.���go�{�"��y�Ί:R������zA�y����k�[��#�X�D���XQ]nQz���e���:uq����9���(���k%4���X	>��=WB��_�a��+^K�.��=(�ݸ7�]l= �ߥ�o+��]F�ٞ���=J�ӕ��r��*n4�k�n���y���J
��(��W�kc�=oe�{Y;
B0J{����P#��5>}�\I�#����{r�V���Bk�[�/+x�J��= �����(��Gj�\��2=�B��/ʠ-�yه�V��19����Ӌ;�r�m������WR���q������������=������^��������y�����[�C�M���Z�Jn0N/�מ���yy�imz��qz��Lޗw�V��;N������ŷ�鳿���Gv5���헷��v�8Hihm�~��h��)^>��^>����H�'�/��h�������'>kÒ��g��������~b4����2J{����m���*g��-F���[�[��l�ḭ��8r�%���o�VI<h8z���>����@I_�ג?��[�6�7�ҩ��6L��m�f4,7��&}mL����rF]��zZ_RL�FE���ް>�=��ٍ�n`\�YI6�S��﵁�p5�3ԁ�V-^�����zZ�Oآ�g(�׆w�cƵ~�n��7į����V9�F���*�Q~p�#gO��[%:�_�iy���~����P[S����b����������3���w��2���0��u�����mm��r�}�FD��/ޅ���[S߅��ɻ��ա�p7����=zk��Pp�������=.z�<8z�{�&"�k�cb�a�����u;�t�&�qۤ�IM�V�~��+����A� 0�2(/�(�mJ$�a�yP^k�{ؚ�" D���:Z�U��
,���V��0,�u\�"�1��ǯi��0��a� <nԁjpۈ@S���0����[�v�sU�LA���)	��7p�V�c0v��ڣ� �������*�m��������6�8����A�nP��rd�:(5��u�5����e
x���
^3\��)`t�CL2��f�ꃘ�Oy 2��^l�����}�����ڦ���]�:ܘ�:�U��ßc��͙�� �M������lܔ�:dl�bhG�Q;��*�O��A�Oy ��W��m��=�.�a�رSn+����ת�^z4o���
!�pT�#���B����)�5*��`s[�_#}%x�V��1_o�S @,�X�Dn���g��x�aq�'n��m��7���	���0k���0/f�7��5Q��������V-����'�dO �n��ϰ�xi5�<���+�p�����R����`�(q` ��҆AjvE�8��N~��!��޴��f��@�8ɢ,�:�ux��&�62�F��Q�?vݴax��ҡ&����Z��+-��pԜ5@5y����2g���k$�::N�mO��+jJ��%Ǫ�	1�*�JK h��%�,�'� �@0��H�a���W#H �o����9����^Y'ԃ�q\��n��c���	o����b�6)�m��SƜn8v�8%,����a���9�����K����m,�ڎ�h{<XzLEI���[�-H���C�S31(~�n��L��+�X~�\���S�u+�L3�[�7�x������(bZ�߼�������Z�^�P�pX�Go���2+��#�g݈Y@�Ʋ�M(��_���������w'�=�6�5B[�B.[�6����rP�0�ޞL�{�����%7��j8�`��#O@�@\*�*T�R~�:y�e��a^3$�ћ��D�)hp���~�/f�ݔ�ZT$��-���+ޗR�s0p�� >/����6�u�뺑C�P��p�]p:���6rPJ\/;�NZ��x�%���N�`^s�`3���6�)��{�3�G�*�j��L�K�� �����3�ȭ�P�};���T�}�uD~����j�tb1�[��^��}��حb���b����ӳ��J,�V��0�q��FMj��
gĴ���l[�~�%�dj1L�r��p}�\�RU��F�+
;� ��TbxMf~kM�k�jF�l)��Fm:&��߁�:�`����[N��Pv��9�;�;ZNj������[1�^�~�&��{����[]n�0�][a��/���ǭ�ե3�[j1L�C6��}�r��Z�>`t����8~�;��k�4�mr��0yc�u�`^�����+Шߕ0�u<�������[̰^��^��;��^�.��
x�Ϗߺ�K����������|5�y0z{(�}W1�,����iLw��w���R~���(���j$�<nߞxW0(Q��y��Co�u��G�+�X�u
�� K�Y[+òvr2,=�
.D�U�����c�d��^X_��]����w����\��]vPu�yW.�cGɫV/.ܻz�G~W/�m��^�s����똻zAkh�yW0�������YY�0z��P0h<��`�V��y��U����[t��+�5Ԋ�c7{��w��h����*9|�@徭��P.l�̏��x�ܾ�]� 窽+�lV��Rå��q��]�]�\���|����Jc�B� S����.��x���Eϕ��I
�q0r�=փbAG��v�bAGa?;�\�X�qV�`��)pRtW,������tW-�in��Up;Qw�B�6�]��'�׷�%��5 �)�L�}�K��$�Z )~������Օj��c��ƲT,�x��9r���>�FÑۗ�Rj�����V��px��v�j���nGϥ�z�#��9���H*���8�1TRU���Qe췇�R���ئ�]>� ʎ�˪z�;����o���`��@uk�R0,Q������dB�(e�y$lg�9��R�:ރ�s������0~$�y�)����GRA#���
܆��)�\I���:)�0^���T�/���H)p��x$�.wG��J:����P'<�����e��zN(6��9�#��_`�~$'�`e�T���w��rW*��b�?�� �	:�r�9���5��pb�H,���GbA��c�#��Š6=R�a6����b�I�#����|$�B'M��}�M:VB�>G�Grv}$�m<�B
j{�/�-�	C��.�����'��4?R�����Xf��~$�x���(��y����;(9&��K�%�
#��kr���|z܈>���*�����`0��;�H0�N3	�nh�O0�N�	·�N�A�8|$����b%T@�#� 3����S~��I�%L,�Ԃ�t��H-�f�F��,R�xOK-r8�e�Ŋ��ĂR+H,\D9���x�E%�S��E���\_�cG9p�3����ñs[u%�L-��7��Z��t<~�ë�ͭ��� ���豊���́�x�x'h�ñ�z'������x�k-���c�1�ݰ۸�����L.ֺ�<�����b��!` ��pQ��b��}�gz�և�������\
NӞ	�	�~������;qQ��b����P;�3���t��^ж�=ӋA\�อ*��􂦿���U�5�v�������L/���>��JU�\��$=�B���b��3��a@�װ�E�y��I�L,�Ep8{&��;��G��������L,�\8���L,�9�����@:\��Ű.�gZ��[��3�`ſVziŉ'���r�r�
����S��9v,_-    ��b}�0�gZ1L��z�9st�{���]��P+�H���L$W�tC��RXU(@\��\�p��a;pށ�Z�����S�6$9��[>p:�T,��2q���6$���Z������V��f<�
���N� ۂ��gY�uj�Z62��j��K��i�NƧZt:�T*��#&7��yɰ���nq�T*���l�ְ�R)�1'�O��J��{]N�`F�a�����X��V����
0���p�����Z���N<��p���T�����_j�n����}8~�T�K� �l���!$���b�������9���
 ��`��A{�Jd���и}�B�jA�
�E�K� �1���c�~�@���2+<a�����:�����g�q��R#�P�� �6~��0ͻd�#9^�Nê�|TU	����D���K� y�R$�췂#�"u~�����|�`�~�ݮ���a"��K� 7-|Y>���K/%x�D��B_*�]���UXb12�p!T/Bl�).��z)��H_
�Q��%G�B����%�Aɭtہ���T���OU���_��蟗���ԋ����>���y).][������JPi�9�m�`$Q8z_9{%`�_	>
K^)�
.�^)>
]�.��p�ݺ�L ֔؅����q�A���A�<X���B!��MV*��ā�U�O��Y�+q�}��J�8�{�xNx%�4'1��ax�Krv�-y��A�'�������+�`����������h�����f���7p��:01�I�S�3�w�n��;u�����<�g�9�<��!~��ȼ��1a��h}�,�hC�ā���8�K��w�`~m�<����CI���.�>1�	�	w X:v(���B�ΨxR��#V��L��;�ș��I��t��F�zQ��i�p��w"�X���� x'�W�9����w2�x�	�?���=?� 9��K'pf(3�gF�O(�6�wBޅ�P���!�N'n��tb�/�r�1��z�g��;�X�+��Û�x�N*�0V�i�p~��w�I%�Ԃ�d�ߩ�����K-(_b�?c������wb1��9�E�j+� ��~�L�y�L��O{�DL�|�ԢT
*3�pP�h�N,���m�Q���Ă1�a�X[�N,�Gk��&����6�`�E �eG�C��Z覲2Rbv#���S�wjAèk��D���\�of�1�|���n澓�	�E��M/�X��y�8,j��E>&� ��U�w����܂w�����#��%�=��3L��h�x'p��ح*]��S8:{�84�w�A�E�	���)F+����Ƹc�TR�;�(�A#� ��e�Of�_fE�A��n\F�����O���a�	�%|$�8��I/(Ck>�!<C�}��(�n�\�k�cf������OrA���OrAy��?��<��Ԃ �f��"w/O-�u �X�]p��$`���bՑ6R�.1Dπ�m���՗�q�Ԃt���Ԃ����� %{&��=QQ��tuRq�ٚ��Oj1�<�X�� �q���s~r@�8?�NO����ZƱ>6j�I})��$��e����{���kFJ��Q*�[:�}l-�F?J���R.��T���7�Q)��>}T
��v�7�[��B�(��z�C��G� #��V*�����ߏR��D'�"���P��$}
���ܚ�B���_�F��*��>�D.X��7��2�[��L�s�~�	�*b���2����G� �_��qCr,��>e�+@""#���հ������Q#�<���fĎ8n�파"�{X��G� ��(���	��,�Wi���-��*�7Yg�G� ];(�B�r��e�rc�߹�G��]�����D ᶂS"�L�P%B���M��I���#�<��Q#pl;F��8ߵ)%���D���i�3��d����v��+"di,�����f��U�!�����(�|�x2CG�/��7$t�X~��~�P8؋>^�<[��H���Z�X~�&�ܝE˒���d�L��J���A�\�}�4�f�3�gH�@�C"��1��BM�,
��;�~��ʿⶉ�����X�5�b����\�0��q�u~4CщsG$u}�J�|)�*Z4�&�K�Y��17�!��3�v
�2�1|i�P��A�,�+�Dd��4ȓm)E�;�<�����̔�M�@g�'I�K��o
�v�>�b۾�J5�6�=��ԡ懤'\wp4���=ݍ���IQ0�f��g���n���q8](]��rWD���0CDݎ�
���귷Ȕ����[�ExE
_���[�,)˨sy?�e���@�-�{�D٨8�E:�L�#�
I�3�tJ�8�k�i�JB��ob�B���b9���X2��%7L���!���f��`p�9C4�6]M3��D�����&�k��=լ�"�y��?3�ԥ�������i�c`U#B�c�ֆӟr(�����e�`�(�o%c�<p>%*��oK�X�^ɐ��t���NBĚ�eIA�gD�� wD���[nuD�7��!��5�|Û�?����rCD7�g�2Ocy�=��'�oJ g�-/��,@`��3ȓ�o-	�!�{�P�aybp�2�<!�xy���o�bH��g3�9�2e��xEL�|��Z�_rf�=M�^<05�s4 �����b9CY����Eh
zz6���pp�����Ǟ!�N������2r�h���K�#�Q�õDԠ�.����M�Du`��Qs,ICA�3H�sz�T9:�x�D�A#O��li~�&I3��eI_&w��lzn�Ā$�i%I�/Y�x�oc��OGL^�$�[���=������̕1���b��p4Wm<C<s?��	u� �@wD3����҉w�G� 8��A����1\,�a�ڼ@�D%�	0�4��Ȅ�h"�����̰$r6{�@�r9���(_���#�	�Ç$H�}@L�p4�P��'H\�Gn�h�i�G��xf�#Y@�D��MC�,��A���q��6����&�K7l��ĈCs�r�5�%^R9�FA'K�8W�czf��[E���֮��
X����i#�K�{AJ%�Pj��do��Xb8���54�/Ü��A�D@J��a�~���́�Cf���!��i8�B�Ι!��DP���ِ?�O�����ݡ�/�j��?P�9���|E�=|!��ih�(�Z�-��P%ީͻ��D���.���	+�a9�ρ#r�X��s�T��.)+3X�AD�w�%8}.��[~��
��A�3���%���v�5���|n���׺O�����i^�i@�0Ĵq�Q�0��Ai�;H�5&̗Fs#,o�M򘋔��� ��錈��\t&Z薌��4-%�Jޢah�k�x����� ,.�59�GH�@��� �v���'��3�S�	OT����g�e~�z%�c�a)%腧�~\jz��� ���c�P�]J=�ñԭ� b@Z~��nLHT�	iX.E��0DR�V�H~��!�.|g$O��
��3�!����YK�����]!O�)*���@��W4�.]�h���f�&����N K9)���S�jůa(,n���aZ�吇���ۘ!�z�{DD�"�Q#��R%��Õ1ĳ�i}o�8��m���yu��D�4�){L�q'A��Vk`I��2�`I�b>�� 6�v�$d�Ä/���f)e��YKj����C��2V%���>�������10$���cǀ���x�=��Dv�{�����M�O��v��.n�V*;�@-��e��+�!��D�G��FR>;DDQ��P��#�_���,霗$D����n�bi2�y�Qi��S��c8��ۉS�θJ��.O��"�RS!�f�e��d�$BI�!��N�$����@o��5��qtP	Pa�h �    �wGO�p7^�<����h��_��^�'Y��8OI��Xٱ1��A�V� �[I�Kt�`$��4٣g�Ӏ�N��SOA
��v��/<'���w�Ќ��w85H�@�g"4(U��{���!V����4�c-2�O(��3֖����|���徿��88�:��I�"���u^� OdY����y)K���7G4`XѬk�d��=��x�Q�r�1�*	�qX�O�Z�]{F,Ia�����^"�����=�+�I��QZ��5L`0Ȕ$��He����L��{��2%o��a�v���{���B嬲d�0��Kd�
��QkL�0!����O��q��O�]���"����/)"墹]����0�"�E�TWh8W8O���Y~<�cw�O��'y�*A^�Y�<�|��V���7wA,������w�UO3��� �UU�<��%ʒ�p&���$X�*M^��U��Q��EJ��Ц��t��[�iD�gɵ\�aإ���������Eʗ'��6v�<qr�IJ�'<����y�����^	��hͩ`�d�׃÷涒$ͫuFy��җ7o�#3-�����y��i�.~��Rk�%�)�R#����Ԩ�i'����M���zg�,��J�7���tY�T�@~�0<��<�;�F�-G5"&��>M5�p����k0cfW@� ��a��0#T�W�SGE�x� b�WJ=f��b��@Pp<�n�N�"\�+�"�C?ʫ�[�fyL�pMD�(u��w�~�Xz��QZ����Co ˒e5��JҸ����A�$i4c灛����\�{�R�x\�=�B�ZەeO�jvyp`�x1D��e�P�4�ƨip#�L{������٘!�FVtE<�`��x�a��R���-�Flj��sňZvйB1���ň��}
U��Ϫ��{�l�Բ�{m�'�-��A�˰<���(�lɰ,�����{��� K-.J��p���{�w�ڮ�{{�V���{f���c`��gF�,r�OOɈFD�.�R���T��O0���4fM�4|���J��p.ߠa.�K]q�%�F��D| ��ʭ��:@����7�X	.���	ʐض[�
x-��T�T�qW6>�0D�tH�B��q\��Պx/�jxU#���/0R��E-��o^�q�:J�'8z��U ��G�Q(%�мC����|#�]"���?@�+@R�R�1��2 �� MR��&j��<�>!�A%J��p���'��`�]��0r%iJ��If8�}͆�����m�Ͽ��]!Q6��q,G\��ċ��R��������9J�'��$��i���� �D�����.�u��@�<-'Q$@�p�ޒahV��q�.�J��J^��4�u�x��8����'ē��0���'��������J�'ޣ��#���j}���H�X�?���*q���􇕪��� ON}pa@�+���혒���oR]���g��f����zd�ck���Dsϯ�!��>{HD�`aB[?-"�Xb�?W6��_CLW��~��� V2���P�����Q2?БC,�Q�#�ܔ��t~L�}D$��3�'���bO��AZJ�9,9�[��s��b8���10����g����~���+�C˅�M\8����*���'����m���\)j��~R�C�e�c*�=��~��G��a��&i�"��<�C�>���1[�+bI�Le���{d
neP�?&!b��s�A�.�e�1qՓP�?9������^ K��M�pg�)���p��%�khN^����gJ�'���S�M}��L���K�9sN�R�1���3#:Cˑ��I a׍+�p���T�a-dy�����!��+"j���
u�ő
���dʿ�qzr2D^F����1��  ��Q{W�C5є�3 4�,� �]��C�o��<,�N��5%C7q�'"�c�����(��Y�$C:ᗤC�M�4��\�ˎ�p��ǒWD��X|D<W}i2Կ���t&��1��R"� �%w*��2���DX�³s0�D�Qs�7�@N͙�CRM��� ;4`�(���ū``f̧�F�muD��9t�(^;hbԿt�[����὾89"��}��
��V��+$Gd��� r~�z�ق���-�HiH�� |ή�� �oud�{�1��aJ^�O�C�30�-� Um����@@!�&�ӱ�Xӹ�N ��~M	z�!�#s�g�^O���N 稵C'�Q� �ﴞ�f%�N�$a`��e�ޡ"ap\� K��Y�����w�H��u���Nu������4)ۊ_E3��ͤ�J	R��h���4�T'j�c08�rEDiwV��f��f�"o��-qͻ��'���L��T$��1bi}�W;_ �W�,6�gȒ%uA�2@���A��Ҳ�L�j�'v��H�!W�CR�Q<�
�L�;�����m~1���8�7@ZX��� �"��T�O�`�Q|X(H��K�#��v� �e��
��2�V��T��=+z�S����q,����H�h8����F��p$�!y����� M��T#sܨ��'�N��u�Yo�":� �B�Gx?<�#��:��T9�>��z���T�ȝ;���;�ܦ�	��E ^Ca�U�ȭ;[F@v�J���.���"���Du�ցXAR*�oJS!"E�4fu̾�ϔ&�P�����S���;\!��^mh��"J�@+��& ���Ҥ?����q�����^O����`�=0D�_|V'�>اtD��+�e��:� ]WCD�M�:���C� \O�pIuL���s
4������wNAi���N*��z��
����* ��=�N* ��a^�y�n֎* ����
ܾ���,Eݟ�9v��OH��VT~"��7����D�#)�Dh��4
C<��O�:�'�R��1�5�M|ID�y������#"j�&�
�`�$� �Cd���yF��- S��0;� ~r8&ALT�N. ���r\e���[)2P�� G�֧�&@T?GH�Y���0H�|z��;��|P2:� ��k���1D�T�D��Z�*�a��4�ԇh���CL*m��)XK��iK�s0 ��inߕ .��\��d��M'��zvF;��l�*4�a�]��2 ;մ�aI�!Q_I|���d���ݎ3 u\�C�D	|�$�6���^�RG`8"j���7v���ޱ���g&>���0���r���#���N���n-�:� �U��d��0�ɩ�䇕w~��7 �l�w��ǫ���6o�p�q`��T�wȓ|��,f08��$�g��c0���:0���x��+��: �0�3���o��5CD�G�����[��(��t�< ��Ӊ�^t����b�^7ͽCH0n��SL8nUԱ֜Wx{@236/�d��HI�`�"�;� �?h�?D8�w���r�İ^�A�k|X���{�4�>��S�&h��@�3N2o���e�,b�|�&b)|x�@3 �<""�w
ty�h
Dp���� >N��BА�uY�g���0Е���
����!�x����gtZ��d�4�!3�����	6��F��a<5������S��6��D�x,��[0�50o�SQ���� DHxg�+���>�5�g#�QBp$�@��^���qw�G� !p�OU��i�q�{>�J����,i�%�f(�r=!�Be�@38(�jʗچ�b�F�0�I0_�΃�gƠ8��n�(W�s����a	e�����h`C�4���K0�3v�<]1Y]��f>���ǳ�>2K����5��x�F�c@��̲��@�W�X��/	���L��K����݂i`"������<@!\CA�Nj~M25�����wo��\0Ȳ�f\������ɒ�ќ�dIp��? �  �4ٴ\��2�B�G�6C4'c�+�wx�sWĳ�gē.����w	�D�h�vש�cY�!w��T�F��Y�/����!ȗ�Bt��O����f���?��� �
��(�~z������f�(0:h�)M�y��Ds�πJԹJ�)�>� QB>��� Q&F��Qspׂg��>hˇ��	Dak�i�������5CL[�R�4��Hw��;��w,��u������w	i�4{�;�!b��=K�SH GR���lj�,��H~O$�!�F>�R!<��!�pzp�,q�)�K��&CP/I����>�
1��<�!"
Хayʾ�1v�2�<Y��`�A��8��A�|�c�����-��q_��3DtO���F�	��Ĉ�8/C<�cf8�����he�μ��3�R�}XR�R�MRĺ�|zZ�κ�91b!>,1�g#�B�,���ɺ]A�A�x�N$F��*�Ĉ��S��QI=#�ĞO��Qu�hjd||_��~7.���H���t��C�")�"Oi�E�5�������4��G�Dl�3� K:��1�,[�w�4Y��
^�њ���u�e�a8-5��pWH�5���C#�	���ȯ��pDW��"��{A<?�!�Q��|=F!����ܯF*�M�x�ǋ�"fJ�&��\7���c`f��æ;�3Ȓ��h<DA\���~��;�,i"�<�P��S� ��� �P��h)H���ʄHG���Β<[�4!���̔'�)̔�s����x����\e�I��*LB� ��}W2D�;�H�08{^�o<�mgL�1�?�q\mm�f0�S�`�X�
��T2�����#G7�������˒�6��>�j�Kz��⇿��𗝹�_z����/��l�����YÉ��l�ˏA��G��Q��/?*����H���].���o�>            x^e�I�#;Dת�d������?�p'��4��$1;��������~}������y�>`���4vv�_���-��a��u��#�m������O��|��󮱟���u̺\��h�SX5v	{^��1�|�_,��~���y����Ζ�J�3&+��&#ڎ�����Ť���'�Xªܯ�U�䪓p<5�&W]���y������a�̸��,���I�k�c��c22���Rb{�+�^�������WO�H^�kOO�?y�����G�ap��1������3јN��s	i�Y�گ<z�a�ቀ,�8�d�+�*�T�,��W�RA���+O=#��3������mz�+������q<GG�Y�|����{�J> ��!��40��y�\�0c{�;�`��������~T�ۛ�� �no�j`���}t�!*oo��.׋�d׃���7@C���L�T����"%s�"��OO�0�Ѧ��7�Ee��r��S�
��}���|R����I��_f(�����۵�}�����*zM��������Xcߗ��
9��%˥�I�-���?Д����x�9�_��j���/BC��>ՂBN�"-�P���ϫ�[V�v8�px�#�a�$��J� <0yo#�QG7�V�BN*�$����3uQ�n�{��2�v�j�1��K8�;�����dS���ƺU&�p]&U`Roǌt�<J�d2���G�NBLf���$��� �Ű#���\
�C�5V.��+�����3���A��bY�BmL�c����5�U��u�	�*�]�xF��oH� CQ���$N���Sɟ�CLF�0Q5�{��N���*�U��x�>`�'Z(�K���$^�<�L��a�Rf���d.$^�&����°#�]}Ͻk8�\C�
4^�E�XQ����7$�(� FbG50E#�uJ�-pjz`a���$�rN3m�k��d��,�F�Y �h@��Z�H|x~aD��p�A��1+� �j^�aG����W�}�YvX��LWg�aqw��e4�E�vX�>0>�aqo'F�����{����Xر��T�?Y���\�m��i$�E�v�IN<��� ��EY�C�"���Qj����E�vh|�'�Hwz�cs80ً�}����j�b�"�"��ym�z�4>�d%���Xc�c`�w����c���r�kL�`�+ژ��]aʿ�F<��s�9	�;�������dƼ���KNvPD��jj;�U�
�<Ҵ����q/+��.#aN+|�=��Fy�F�C�>XN!���PC�q[J�휐T�O���h�h������{䡊IQ�X�hc���xu�Q{�>�c�7zY���Z�nQ˪��q�������N�����C�F]�8���o�Ŷ�[k0���R+;�L��3A�y-�n�/BQm�0v�i�u�Ӹ�:��'���D�#�!��+�㭲�<�=����-`2�lb9��W���0�&����ʠ8����-q�4�VG�ǩ�\�邏���.N>X�`��|��t��x�ja8�uv
�hu4�m0���(6F�Ӆ�Vٕv��w��JL1��+]
Î�L1��}o�����{���Vir�&��;�8���"FG0yOg(�ZBy�q<��q�F��%�VD^Y�\���3�qpjUĉ<>�0���XA��CC8�ŔS,�C�#�0����r�P��8ͯ�3Fm��d,,�}��~,ꝥ19�C��1j�Ǌ����p���khAGyH��Q<�&�����Q�	�b�C�L��ëZ�d^{�¨�����{ɴ�p�:�𲶰upҲj^>��x�S[%���0�d.�XML�������J���5��L>ܼ�8�gR�)(��&�]��&sX�L���#�{�3�1�S8�R�C�D�r�Î�'�<RÉ��maGֹ�
��΂Ɏ8���
�4����a�!E(�&�CL���v5�16�CNV����s�.X����ѧ�5&kU���UU��1���&c!�ԣ��"� �se��h�)>A�ɰ�Pϊd6cјӱ.�cϺR
c�R\�W �Xčz�".=�F����R�X�(�E�GPx;��C����Pe��b�PązN&��窅�3�,���w���X�I=�6r��n�`�g���0xm��-\+���3W�d^=�0�Hσ)0xE,�q���Ӈ��	�W1�63,�=��*\���«96J�r�:��ډ�E<N(|̷�Ѩ��x�p��ʥ�2��k'&ۂ�;���3,>�U�:�J��0�u8�}g�x������IU���	MLf�ڴ����n�1�0�#�La��q�L!��tUa-���	��H%�	�W0x�2F0j�z���t
b� j{���N8��&c�R�
�;`�c�f�^a��'�8�H�j`
Z�x[�0H��P�;Q�vO<|	�ć~�� �v�s��Y1����*�^\�w,�V$[�z�;���.w�I|̧��I|�!�ᵥZ�wg c����<�ɴ��+l��z�;�×i��өJ�(��_�|'^IU����欄U��īS��\|R�Zo'k�T�V��xΓxa$UFh=��U�@0Wn/,,�7HH��R��M,����>i����eb��b,+��u:g	cc���<��X��[P^��
�[H<�,���^��v>���f�0V0Da��E�gܧ���2:ݔI�"�ǯ�'?R`a�b���g������/�4�xC� ŗ&��yƛ����dE����ƚ3���B�������*�Pxn����,�x��\A�=�����6cA}b�����k,_������3���7�r�r��I�o��|ś�PEX�s�����Ԁ/γò��F$_W/|������K%�O⭲2���Ε��E[,a�{w[}!u`�+��;1��w�S=c%�R�w�̷0�k�i�q�?�</��-�᫬�ۮ��/�^ɷ^u/8<]�u��JOW�'���b
8��t�zd����wa�ږs���+�������!'c�x�=��z�� �)�x��zNy|U���e���t@
w�w������W��~Җ�¿ٹB�X��x����l��UzV�z���*}uѐ��4��<j��Xnܥ�WԨ/*y@�c������߱�12j���[+>.���m�W<�*�� �K�e�0f�
Ê�|��J����i�b�*���m*� .O�����MBLg���2^R}gG��8�ǋ�	}��������y��j�}�Mzzt=�\�w�Lfg(l}�&�݁���� �c*9��9�Đ3�Kz�*�k�*��-�~���r��Ѡ���iorE)�|Ƃ���r����(��_��WP��N	�ϻԠ�<�t��x�ea�!�1�
��QbwPx̒�㻶�.<u�๟��� ��A�P��na$U����-d>��W�(�h(�xbZ�7�u�p�11���5Q�I)����X�����6sby[8�<j7�q
WFN�Xd�W�CgaA�� �5�߮���!q_�M,oo�)FQ��c<$�[���c�M,Z����"��8�w4�A�br����"�o8��71H�#�vs�wmC�V�PC٩<����?��p�����1�08|��⳶�N�y�x~&�|�6���+���]X��Z�X�5��Io��mnX�x�<,>�V�C.X�s@��U��[��K(� �/�_�z	�Q-����;"�;>j����!',����}��uc�3x;~ayˆv��oH<�
�(l]Oy���������rJ�8�g�&����փ��*�竭��ܘ"G�!gl}`1�Ϊ�q��)<�_X2��j3q��>�,��}g9��z��"�AU�F�j繫�g�צ㎏�2܅�Pc]#��������
yR��v"w|�>t�ѩ�Y�����>Pr��Ugk�qC��^�wQ��#��|Je(���cC�����S��=Px�aayYh������-,wT���}�-|b��11Ҫ�Yێ'.҇���#*�??px�Abp��5� �  q�\X���|�mzے���E���ի˃���>2��X�mƭ�<�$7�+���P(�8�Ì_r��Ŕ[�����2}5F��
��TCa#�H�a�F�e	ax�
L���}޲*��1|B�����1�X���W�6�S���m��o�>oi���6�X~�n���'(<Ӷ��-,���_r|��U�z⋶��1��C=c�1�S�+���L6�5$_����:��6c�mB�1!���f}�ąZ�����g.��{���~�@�է
�{�!����S�9|8���3Щ���o[e�B�������Vdb��v�{a}�n9cc�',�_�K����C���\Y���a�XB�0r����h���p�r �^6�0����&�3�"7�c>cyG�u�����m�/|�� �^c�Q���Y�ea����5VߦGw���Sw�c;�Y_ry=��͘j�W��?�M,��aL��M��H����/{��X~*����mUa�c�g9x#c�/���Q��-���R�r�9r�(0�|��[Gl�R��w|���3D�gxK�4(l4+��Xv�m������XP>�I��2��F{jad�+9�eD(��`y����/l0Ga�7��z��O���,]rT�0Wѥ�����y�OX�x�>�:�`@�q�m�/�p_Y.���`��f�0�n۱� ��#��w��g0���T%F���ץ*�04�&F��ZrTG�wa� �U�a���埳���V�U�a|�fl�`�EI]�S���A�3�W^-,�cf],G^��Ra�"Z��uu�-,���|*˸So7ʿ��8�wx���D�ϰ�[��X���N�A��3���M1r��GH��Ocr=y[�����C�6R�=0�=i~eo9c�����,��Îܻ�c�x��2*����s3s������i         �  x^}W[r7�O���}��2)�DI��*�pZB�b!��[*G��,)�q�cQ�`0��'l�ʱ�%3��o��7��h���t6��bZ��9��I��g���YPH�.�rR6|}����Q�(f|��cg�#�|�f���x񆯥p�(\��|��%��"z�Ҕ_�����+���e�4�fŤd׽0�N8���4�����R4Ǻ����^��M�%Nl��[aTͿ��� ��*�'�z��]�,o��;��O�6x
.o����"^�-y8�`+嶊�؍�w����l��1����d�>v�lH@C�,		��Kg�ԑ�%�i��	Ťc�J�z+[�on�Ȍ��Wwg��I�n��xܝRB����EΞ�(9�LΪN�iZL��]K#�֭� ��_MC1-��d�U�W�2���	�bO�j�#_�.��%_�C�0��T5((�&s����5�I� ��F���I�A�$_nmm��y�j��:�0�+Y���4fl�z�h#��D�Z4�*G��y˞����um2eF�!�b�$LF��k������u'7�mX�;����4cOޘ1(0>�P�ɑR`2�f@�U-����S-�aNؤ��w~)��Wwַb�X�rGo���V��<�ҁ�����S��)3J:k
���M�IZ�u��m�8��Ђ b�)�g�.��G\����}�?`���s�ێO(�%��߭�!&(�Ѻ�>���B� zt�	��	ƶZL�����wz;�H�����(�#���i1��L®m�Z���OR+c�RA-N���n���p�����c��V���8�Q4/�@#5��	�g1M������Po����!̡5Y�փ�Z��`۷U<0>+�G�EWZm��b_�ƾ��k�vT�/�3�D:ZP���8P������'�e޴ ��^z'�����Ю��{42���H��} ,�94w�W��ڜ�6��+��$�GQw���O�{�/���?5�?> �t��bZ�<{M+��a���$�*��JJ�2��Qli��y�>��/��3������PX�ɉ���$�%!�aȂ��]���{���N醊���/��d�l����+��I�+����$��FjRltrRژ-��8�q4#�o�R`\�Mi�
*F�tR�4(X1c��YE��|���6a�J��"A>�v~?���~OVM�Ng�(��=eWJG�/"�Gk�c!$c��m�7����P�*^�B���A�^����5�E;���[k�&_�b`�\@��ō5F��p��^�KqtԢ������R�o����D1gߓR�vp�A(����qΏ��X -֗u/׀�^�8Y_��r��I��?(lF���шvo�i���e00����l@��ɉ�g{]:��˔=�������6���/�"2��l��p�m�n.���)�}��_�n��Gµ�/�3�JM��4�D�(vk�rJ�Wx���C�����ڰwXrS�.�Nӹ��l�=�������	!T�[�[K�o��@l�^�{�O��9��=��Z�nh;�j�8Mm4�r�h�e�O#��� c:�zY��j�����W�՟����&�JC�w��t�Z4pw㲟?�/��q�VX،��y�D�*c� ��.Hc��^D+������%w����;Q�6�<��x��7h��ٴ��nR�NUh��:�U'a���ut��b��j�r.L�1������	c^[1.������d2�Ӎ�\         �   x^��N�@D��W�P�I�=ҪD�%W.npY�M6�u�׳\�i捃&�9�%�jt�o�
��r�gz����/��NLR�a,�[o7p��ѩ�2&1�e�E�9��9h櫘�t�l��,A2�->Có-�Ĥ&t�"Y��8j��8	��)�����*ܗ��E�	8Lq�=��WI�����_^�v�6�j�tqY'z˹?���M�     