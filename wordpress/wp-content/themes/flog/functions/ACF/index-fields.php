<?php
if( function_exists('acf_add_local_field_group') ):

	acf_add_local_field_group(array(
		'key' => 'group_61d3368953eb1',
		'title' => 'تنظیمات صفحه اصلی',
		'fields' => array(
			array(
				'key' => 'field_61d3381be9613',
				'label' => 'تنظیمات اسلایدر صفحه اصلی',
				'name' => '',
				'type' => 'accordion',
				'instructions' => '',
				'required' => 0,
				'conditional_logic' => 0,
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'open' => 0,
				'multi_expand' => 0,
				'endpoint' => 0,
			),
			array(
				'key' => 'field_6203dce5163f6',
				'label' => 'استایل اسلایدر اصلی',
				'name' => 'main_slider_style',
				'type' => 'select',
				'instructions' => 'از بین استایل های موجود یک مورد را برای اسلایدر خود انتخاب کنید.',
				'required' => 1,
				'conditional_logic' => 0,
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'choices' => array(
					'full-width' => 'تمام عرض',
					'box-border' => 'باکس با حاشیه گرد',
				),
				'default_value' => array(
					0 => 'full-width',
				),
				'allow_null' => 0,
				'multiple' => 0,
				'ui' => 1,
				'ajax' => 0,
				'return_format' => 'array',
				'placeholder' => '',
			),
			array(
				'key' => 'field_61d33845e9614',
				'label' => 'نوع اسلایدر اصلی',
				'name' => 'main_slider_type',
				'type' => 'select',
				'instructions' => 'انتخاب کنید که اسلایدر صفحه اصلی چه محتوایی را نشان دهد.',
				'required' => 1,
				'conditional_logic' => 0,
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'choices' => array(
					'all' => 'همه',
					'cat' => 'دسته بندی',
					'tag' => 'برچسب',
				),
				'default_value' => array(
				),
				'allow_null' => 0,
				'multiple' => 0,
				'ui' => 1,
				'ajax' => 0,
				'return_format' => 'array',
				'placeholder' => '',
			),
			array(
				'key' => 'field_61d336a19bf24',
				'label' => 'دسته بندی اسلایدر صفحه اصلی',
				'name' => 'main_slider_cat',
				'type' => 'taxonomy',
				'instructions' => 'انتخاب کنید که اسلایدر صفحه اصلی مطالب کدام دسته بندی را نشان دهد.',
				'required' => 1,
				'conditional_logic' => array(
					array(
						array(
							'field' => 'field_61d33845e9614',
							'operator' => '==',
							'value' => 'cat',
						),
					),
				),
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'taxonomy' => 'category',
				'field_type' => 'select',
				'allow_null' => 1,
				'add_term' => 0,
				'save_terms' => 0,
				'load_terms' => 0,
				'return_format' => 'object',
				'multiple' => 0,
			),
			array(
				'key' => 'field_61d3393da8a62',
				'label' => 'برچسب اسلایدر صفحه اصلی',
				'name' => 'main_slider_tag',
				'type' => 'taxonomy',
				'instructions' => 'انتخاب کنید که اسلایدر صفحه اصلی مطالب کدام برچسب را نشان دهد.',
				'required' => 1,
				'conditional_logic' => array(
					array(
						array(
							'field' => 'field_61d33845e9614',
							'operator' => '==',
							'value' => 'tag',
						),
					),
				),
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'taxonomy' => 'post_tag',
				'field_type' => 'select',
				'allow_null' => 1,
				'add_term' => 0,
				'save_terms' => 0,
				'load_terms' => 0,
				'return_format' => 'object',
				'multiple' => 0,
			),
			array(
				'key' => 'field_61d33753105a0',
				'label' => 'تعداد مطالب اسلایدر',
				'name' => 'main_slider_count',
				'type' => 'number',
				'instructions' => 'تعداد مطالبی که میخواهید در اسلایدر نمایش داده شود را وارد کنید',
				'required' => 0,
				'conditional_logic' => array(
					array(
						array(
							'field' => 'field_61d33845e9614',
							'operator' => '!=empty',
						),
					),
				),
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'default_value' => 5,
				'placeholder' => '',
				'prepend' => '',
				'append' => '',
				'min' => 1,
				'max' => '',
				'step' => '',
			),
			array(
				'key' => 'field_61d33d1632bf6',
				'label' => 'بستن آکاردئون اسلایدر اصلی',
				'name' => '',
				'type' => 'accordion',
				'instructions' => '',
				'required' => 0,
				'conditional_logic' => 0,
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'open' => 0,
				'multi_expand' => 0,
				'endpoint' => 1,
			),
		),
		'location' => array(
			array(
				array(
					'param' => 'options_page',
					'operator' => '==',
					'value' => 'theme-general-settings',
				),
			),
		),
		'menu_order' => 0,
		'position' => 'normal',
		'style' => 'default',
		'label_placement' => 'top',
		'instruction_placement' => 'label',
		'hide_on_screen' => '',
		'active' => true,
		'description' => '',
	));

endif;