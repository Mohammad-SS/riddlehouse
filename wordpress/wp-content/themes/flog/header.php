<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>"/>
    <meta name="viewport"
          content="width=device-width, initial-scale=1"/>
    <!--load all Font Awesome styles -->
    <link href="<?= get_template_directory_uri() ?>/css/fontawesome/all.css"
          rel="stylesheet"/>
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>

<?php
//get variables
if ( get_field( 'logo_img', 'option' ) ) {
    $headerLogo = get_field( 'logo_img', 'option' );
} else {
    $headerLogo = '';
}

if ( get_field( 'social_header','option' ) ) {
    $social = get_field( 'social_header' ,'option');
} else {
    $social = null;
}

$HeaderType=get_field('header_type','option');
?>
<?php include_once 'template/responsive-menu.php';
if ($HeaderType){
    $path='template/header/'.$HeaderType['value'].'.php';
    include_once $path;
}

?>
