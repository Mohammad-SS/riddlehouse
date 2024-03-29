<?php
if( function_exists('acf_add_local_field_group') ):

	acf_add_local_field_group(array(
		'key' => 'group_61d1f5613bcf6',
		'title' => 'تنظیمات سربرگ قالب',
		'fields' => array(
			array(
				'key' => 'field_620176f89b2cb',
				'label' => 'نوع سربرگ قالب',
				'name' => 'header_type',
				'type' => 'select',
				'instructions' => '',
				'required' => 1,
				'conditional_logic' => 0,
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'choices' => array(
					'full-width-header' => 'تمام عرض',
					'box-border-header' => 'جعبه ای',
				),
				'default_value' => array(
					0 => 'full-width-header',
				),
				'allow_null' => 0,
				'multiple' => 0,
				'ui' => 1,
				'ajax' => 0,
				'return_format' => 'array',
				'placeholder' => 'نوع سربرگ قالب را انتخاب کنید.',
			),
			array(
				'key' => 'field_61d1f8d834e31',
				'label' => 'تصویر لوگو',
				'name' => 'logo_img',
				'type' => 'image',
				'instructions' => '',
				'required' => 0,
				'conditional_logic' => 0,
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'return_format' => 'array',
				'preview_size' => 'header-logo',
				'library' => 'all',
				'min_width' => '',
				'min_height' => '',
				'min_size' => '',
				'max_width' => '',
				'max_height' => '',
				'max_size' => '',
				'mime_types' => '',
			),
			array(
				'key' => 'field_61d30aa232edf',
				'label' => 'شبکه های اجتماعی سربرگ',
				'name' => 'social_header',
				'type' => 'repeater',
				'instructions' => '',
				'required' => 0,
				'conditional_logic' => 0,
				'wrapper' => array(
					'width' => '',
					'class' => '',
					'id' => '',
				),
				'collapsed' => '',
				'min' => 0,
				'max' => 0,
				'layout' => 'table',
				'button_label' => 'شبکه اجتماعی جدید',
				'sub_fields' => array(
					array(
						'key' => 'field_61d30ac232ee0',
						'label' => 'کلاس آیکون شبکه اجتماعی',
						'name' => 'icon_social',
						'type' => 'text',
						'instructions' => 'از لینک زیر برای پیدا کردن کلاس آیکون ها استفاده کنید
https://fontawesome.com/v5.15/icons?d=gallery&p=2&s=brands
مثلا: fab fa-youtube',
						'required' => 0,
						'conditional_logic' => 0,
						'wrapper' => array(
							'width' => '',
							'class' => '',
							'id' => '',
						),
						'default_value' => '',
						'placeholder' => '',
						'prepend' => '',
						'append' => '',
						'maxlength' => '',
					),
					array(
						'key' => 'field_61d30afb32ee1',
						'label' => 'لینک شبکه اجتماعی',
						'name' => 'link_social',
						'type' => 'text',
						'instructions' => '',
						'required' => 0,
						'conditional_logic' => 0,
						'wrapper' => array(
							'width' => '',
							'class' => '',
							'id' => '',
						),
						'default_value' => '',
						'placeholder' => '',
						'prepend' => '',
						'append' => '',
						'maxlength' => '',
					),
				),
			),
		),
		'location' => array(
			array(
				array(
					'param' => 'options_page',
					'operator' => '==',
					'value' => 'header',
				),
			),
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