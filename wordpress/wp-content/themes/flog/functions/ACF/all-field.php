<?php 

function my_acf_add_local_field_groups(){
    include_once 'option-page.php';
	include_once 'header-fields.php';
	include_once 'footer-fields.php';
	include_once 'index-fields.php';
}
add_action('acf/init', 'my_acf_add_local_field_groups');
