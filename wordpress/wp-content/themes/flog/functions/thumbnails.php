<?php
add_image_size('header-logo', 135, 40, true);
add_image_size('post-card', 340, 420, true);
add_image_size('post-card-cat', 354, 420, true);
add_image_size('post-card-single', 802, 420, true);
add_image_size('post-card-small', 85, 90, true);

function the_thumbnail($sizeof, $class = null, $postId = null, $echo = true)
{
    $img = null;
    if ($postId == null) {
        $postId = get_the_ID();
    }
    if (has_post_thumbnail($postId)) {
        $img = get_the_post_thumbnail($postId, $sizeof, array('class' => $class));
//        var_dump(get_the_post_thumbnail($postId));
    } elseif ($sizeof == 'header-logo') {
        $img = '<img src="' . WP_THEME_DIR . 'img/header-logo-no-thumb.jpg" title="' . get_the_title() . '"  alt="' . get_the_title() . '" width="135" height="40"/>';
    }elseif ($sizeof == 'post-card') {
	    $img = '<img src="' . WP_THEME_DIR . 'img/post-card-no-thumb.jpg" title="' . get_the_title() . '"  alt="' . get_the_title() . '" width="340" height="420"/>';
    }elseif ($sizeof == 'post-card-cat') {
	    $img = '<img src="' . WP_THEME_DIR . 'img/post-card-cat-no-thumb.jpg" title="' . get_the_title() . '"  alt="' . get_the_title() . '" width="354" height="420"/>';
    }elseif ($sizeof == 'post-card-single') {
	    $img = '<img src="' . WP_THEME_DIR . 'img/post-card-single-no-thumb.jpg" title="' . get_the_title() . '"  alt="' . get_the_title() . '" width="802" height="420"/>';
    }elseif ($sizeof == 'post-card-small') {
	    $img = '<img src="' . WP_THEME_DIR . 'img/post-card-small-no-thumb.jpg" title="' . get_the_title() . '"  alt="' . get_the_title() . '" width="85" height="90"/>';
    }

    if ($echo) {
        echo $img;
    } else {
        return $img;
    }
}
