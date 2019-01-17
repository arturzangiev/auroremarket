# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['auroremarket.fr']
    start_urls = [
        'https://auroremarket.fr/s-1/categories_2-pates_riz_graines_et_cereales',
        'https://auroremarket.fr/s-1/categories_2-the',
        'https://auroremarket.fr/s-1/categories_2-pain_et_tartine',
        'https://auroremarket.fr/s-1/categories_2-produits_aperitifs',
        'https://auroremarket.fr/s-1/categories_2-legumes_au_naturel',
        'https://auroremarket.fr/s-1/categories_2-proteines_vegetales',
        'https://auroremarket.fr/s-1/categories_2-infusion',
        'https://auroremarket.fr/s-1/categories_2-puree_d_oleagineux',
        'https://auroremarket.fr/s-1/categories_2-super_aliments',
        'https://auroremarket.fr/s-1/categories_2-fruits_secs_et_seches',
        'https://auroremarket.fr/s-1/categories_2-gros_conditionnements',
        'https://auroremarket.fr/s-1/categories_2-graines_et_cereales',
        'https://auroremarket.fr/s-1/categories_2-cafe_et_cacao',
        'https://auroremarket.fr/s-1/categories_2-contenants_pour_vrac',
        'https://auroremarket.fr/s-1/categories_2-sauces_et_condiments',
        'https://auroremarket.fr/s-1/categories_2-huile',
        'https://auroremarket.fr/s-1/categories_2-fruits_secs_et_fruits_seches',
        'https://auroremarket.fr/s-1/categories_2-petit_dejeuner',
        'https://auroremarket.fr/s-1/categories_2-boissons',
        'https://auroremarket.fr/s-1/categories_2-plats_prepares',
        'https://auroremarket.fr/s-1/categories_2-farine',
        'https://auroremarket.fr/s-1/categories_2-compote',
        'https://auroremarket.fr/s-1/categories_2-chocolat_et_cacao',
        'https://auroremarket.fr/s-1/categories_2-epicerie_sucree',
        'https://auroremarket.fr/s-1/categories_2-viandes_pate_et_poissons',
        'https://auroremarket.fr/s-1/categories_2-pates_riz_graines_et_cereales',
        'https://auroremarket.fr/s-1/categories_2-vins_rouges',
        'https://auroremarket.fr/s-1/categories_2-aperitifs_et_digestifs',
        'https://auroremarket.fr/s-1/categories_2-vins_blancs',
        'https://auroremarket.fr/s-1/categories_2-boissons_petillantes',
        'https://auroremarket.fr/s-1/categories_2-vins_roses',
        'https://auroremarket.fr/s-1/categories_2-bieres',
        'https://auroremarket.fr/s-1/categories_2-produits_menagers',
        'https://auroremarket.fr/s-1/categories_2-thermos_gourde_et_qualite_de_l_eau',
        'https://auroremarket.fr/s-1/categories_2-autre',
        'https://auroremarket.fr/s-1/categories_2-papier_et_conservation_des_aliments',
        'https://auroremarket.fr/s-1/categories_2-pique_nique_et_aperitif',
        'https://auroremarket.fr/s-1/categories_2-contenants_pour_vrac',
        'https://auroremarket.fr/s-1/categories_2-produits_pour_la_vaisselle',
        'https://auroremarket.fr/s-1/categories_2-soin_du_linge',
        'https://auroremarket.fr/s-1/categories_2-ambiance',
        'https://auroremarket.fr/s-1/categories_2-manches_longues',
        'https://auroremarket.fr/s-1/categories_2-manches_courtes',
        'https://auroremarket.fr/s-1/categories_2-manches_longues_2',
        'https://auroremarket.fr/s-1/categories_2-manches_courtes_2',
        'https://auroremarket.fr/s-1/categories_2-insectes_et_nuisibles',
        'https://auroremarket.fr/s-1/categories_2-materiel',
        'https://auroremarket.fr/s-1/categories_2-graines_et_semences',
        'https://auroremarket.fr/s-1/categories_2-materiel_scolaire_et_de_bureau',
        'https://auroremarket.fr/s-1/categories_2-couches',
        'https://auroremarket.fr/s-1/categories_2-hygiene_et_change',
        'https://auroremarket.fr/s-1/categories_2-biberons_et_accessoires',
        'https://auroremarket.fr/s-1/categories_2-biscuits_bebe',
        'https://auroremarket.fr/s-1/categories_2-cereales_bebe',
        'https://auroremarket.fr/s-1/categories_2-petits_repas_sucres',
        'https://auroremarket.fr/s-1/categories_2-petits_repas_sales',
        'https://auroremarket.fr/s-1/categories_2-bouillie',
        'https://auroremarket.fr/s-1/categories_2-lait_infantile_brebis_et_chevre',
        'https://auroremarket.fr/s-1/categories_2-lait_infantile_vegetal',
        'https://auroremarket.fr/s-1/categories_2-lait_infantile'
    ]

    def parse(self, response):
        urls = response.xpath('//a[@class="product_img_link"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

        # Calling next page
        next_page_url = response.xpath('//li[@class="pagination_next"]/a/@href').extract_first()
        yield scrapy.Request(next_page_url, callback=self.parse)

    def individual_page(self, response):
        base_price = response.xpath('//span[@class="am_old_price"]/text()').re_first('(\d+\,\d+) €')
        discounted_price = response.xpath('//p[@class="our_price_display"]/span[@class="price"]/@content').extract_first()
        product_name = response.xpath('//h1[@class="am_marque_title "]/text()').extract_first().strip()
        category = response.xpath('//span[@class="navigation_page"]/span/a/@title').extract_first()

        fields = dict(base_price=base_price, discounted_price=discounted_price, product_name=product_name, category=category)

        yield fields