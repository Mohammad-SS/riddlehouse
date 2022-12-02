<?php

//includes 
require_once get_template_directory() . '/functions/class-tgm-plugin-activation.php';
include_once 'functions/ACF/all-field.php';
include_once 'functions/thumbnails.php';

function wordpressify_resources() {
    wp_enqueue_style( 'style', get_stylesheet_uri() );
    wp_enqueue_script( 'header_js', get_template_directory_uri() . '/js/header-bundle.js', null, 1.0, false );
    wp_enqueue_script( 'footer_js', get_template_directory_uri() . '/js/footer-bundle.js', null, 1.0, true );
}

add_action( 'wp_enqueue_scripts', 'wordpressify_resources' );

// Customize excerpt word count length
function custom_excerpt_length() {
    return 22;
}

add_filter( 'excerpt_length', 'custom_excerpt_length' );

// Theme setup
function wordpressify_setup() {
    // Handle Titles
    add_theme_support( 'title-tag' );

    // Add featured image support
    add_theme_support( 'post-thumbnails' );
}

add_action( 'after_setup_theme', 'wordpressify_setup' );

show_admin_bar( false );

// Checks if there are any posts in the results
function is_search_has_results() {
    return 0 != $GLOBALS['wp_query']->found_posts;
}

function register_my_menu() {
    register_nav_menu( 'header-menu', __( 'منو سربرگ' ) );
}

add_action( 'init', 'register_my_menu' );

function add_additional_class_on_a( $classes, $item, $args ) {
    if ( isset( $args->add_a_class ) ) {
        $classes['class'] = $args->add_a_class;
    }

    return $classes;
}

add_filter( 'nav_menu_link_attributes', 'add_additional_class_on_a', 1, 3 );

/**
 * Add a sidebar.
 */
function wpdocs_theme_slug_widgets_init() {
    register_sidebar( array(
            'name'          => __( 'سایدبار قالب', 'textdomain' ),
            'id'            => 'main-sidebar',
            'description'   => __( 'سایدبار قالب فلاگ', 'textdomain' ),
            'before_widget' => '<li id="%1$s" class="widget %2$s">',
            'after_widget'  => '</li>',
            'before_title'  => '<h3 class="widgettitle">',
            'after_title'   => '</h3>',
    ) );
}

add_action( 'widgets_init', 'wpdocs_theme_slug_widgets_init' );

//better comments
function better_comments( $comment, $args, $depth ) {
    $comment_id        = $comment->comment_ID;
    $comment           = get_comment( $comment_id );
    $comment_author_id = $comment->user_id;
    ?>
    <li>
    <div class="comment" <?php comment_class( 'comment-item' ) ?>
         id="comment-<?= $comment_id ?>"
    <figure>
        <img src="<?= get_avatar_url( $comment_author_id, [ 'size' => '70' ] ) ?>"
             alt=""
             title="">
    </figure>
    <div class="comment__info">
        <div class="comment__title">
            <span><?php printf( '%s', get_comment_author_link() ); ?></span>
            <i class="fas fa-circle"></i>
            <em><?= get_comment_date() ?></em>
        </div>
        <?php comment_text(); ?>
        <div class="comment__footer">
            <div class="comment__footer-left">
                <?php comment_reply_link( array_merge( $args, array(
                                'reply_text' => '<em class="comment__footer-reply">
                        پاسخ به دیدگاه
                    </em>',
                                'depth'      => $depth,
                                'respond_id' => 'respond',
                                'max_depth'  => $args['max_depth']
                        )
                ),$comment ); ?>
            </div>

        </div>

    </div>
    </div>
    <?php
}