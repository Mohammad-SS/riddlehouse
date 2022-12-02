<?php
// The Query
$mainSliderType  = get_field( 'main_slider_type', 'option' );
$mainSliderCount = get_field( 'main_slider_count', 'option' );

switch ( $mainSliderType['value'] ) {
    case 'cat':
        $catSlider      = get_field( 'main_slider_cat', 'option' );
        $argsMainSlider = array( 'cat' => $catSlider->term_id );
        break;
    case 'tag':
        $tagSlider      = get_field( 'main_slider_tag', 'option' );
        $argsMainSlider = array( 'tag_id' => $tagSlider->term_id );
        break;
}
$argsMainSlider['posts_per_page'] = (int) $mainSliderCount;
$the_query                        = new WP_Query( $argsMainSlider );
// The Loop
if ( $the_query->have_posts() ) {
    ?>
    <div class="container">
        <section class="box-border-slider">
            <!-- Slider main container -->
            <!-- Additional required wrapper -->
            <div class="swiper-wrapper">
                <?php
                while ( $the_query->have_posts() ) {
                    $the_query->the_post();
                    $post_id         = get_the_ID();
                    $post_thumb_url  = get_the_post_thumbnail_url( $post_id, 'full' );
                    $post_categories = get_the_terms( $post_id, 'category' );

                    ?>
                    <!-- Slides -->
                    <div class="swiper-slide">
                        <img src="<?= $post_thumb_url ?>" alt="<?= get_the_title() ?>"/>
                        <div class="slide-content">
                            <div class="slide-content__categories">
                                <?php
                                foreach ( $post_categories as $cat ) {
                                    echo '<a href="' . get_term_link( $cat->term_id ) . '" class="slider-cat"><h4>' . __( $cat->name ) . '</h4></a>';
                                } ?>
                            </div>
                            <div class="slide-content__title"><a href="<?= the_permalink() ?>">
                                    <h1> <?= get_the_title() ?></h1></a></div>
                            <div class="slide-content__more">
                                <div class="slide-content__more-right">
                                    <i class="fal fa-comment"></i><?= get_comments_number( $post_id ) ?> دیدگاه
                                </div>
                                <div class="slide-content__more-center">
                                    <i class="fal fa-clock"></i><?= get_the_date() ?></div>
                                <div class="slide-content__more-left"><?= get_avatar( $post->post_author, 35, '', get_the_author() ) ?><?= get_the_author() ?></div>
                            </div>

                        </div>
                    </div>
                    <?php
                }
                ?>
            </div>

            <!-- If we need navigation buttons -->
            <div class="swiper-button-prev">
                <i class="fas fa-chevron-right"></i>
            </div>
            <div class="swiper-button-next">
                <i class="fas fa-chevron-left"></i>
            </div>

        </section>
    </div>
    <?php
}
/* Restore original Post Data */
wp_reset_postdata();
wp_reset_query();
?>