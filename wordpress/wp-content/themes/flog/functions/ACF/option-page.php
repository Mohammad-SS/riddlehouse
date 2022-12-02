<?php 
if( function_exists('acf_add_options_page') ) {
	
	acf_add_options_page(array(
		'page_title' 	=> 'تنظیمات قالب',
		'menu_title'	=> 'تنظیمات قالب',
		'menu_slug' 	=> 'theme-general-settings',
		'capability'	=> 'edit_posts',
		'redirect'		=> false
	));
	
	acf_add_options_sub_page(array(
		'page_title' 	=> 'تنظیمات سربرگ',
		'menu_title'	=> 'تنظیمات سربرگ',
		'parent_slug'	=> 'theme-general-settings',
        'menu_slug'=>'header'
	));
	
	acf_add_options_sub_page(array(
		'page_title' 	=> 'تنظیمات پاورقی',
		'menu_title'	=> 'تنظیمات پاورقی',
		'parent_slug'	=> 'theme-general-settings',
        'menu_slug'=>'footer'
	));
	
}
