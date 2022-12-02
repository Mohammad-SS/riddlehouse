<?php get_header();

//variable
$SliderType=get_field('main_slider_style','option');
?>
<div class="main-content">

    <!--main slider-->
    <?php
    if ($SliderType){
        $path='template/slider/'.$SliderType['value'].'-slider.php';
        include_once $path;
    }
   ?>
    <!--end main slider-->

    <section class="latest-posts">
        <!-- container -->
        <div class="container">
            <!-- site-content -->
            <article class="posts-container">
                    <!-- main-column -->
                    <div class="row">
                        <?php
                        if ( have_posts() ) :
                            while ( have_posts() ) :
                                the_post();
                                $post_categories = get_the_terms( get_the_ID(), 'category' );
                                ?>
                                    <div class="post-card" data-aos="fade-up" data-aos-duration="1000">
                                        <div class="post-card__img"><a href="<?php the_permalink(); ?>"><?php the_thumbnail('post-card') ?></a></div>
                                        <div class="post-card__content">
                                            <div class="post-card__content-categories">
                                                <?php
                                                foreach ( $post_categories as $cat ) {
                                                    echo '<a href="'.get_term_link($cat->term_id).'" class="post-cat"><h4>' . __( $cat->name ) . '</h4></a>';
                                                }?>
                                            </div>
                                            <h1 class="post-card__content-title"><a href="<?php the_permalink() ?>"><?php the_title() ?></a></h1>
                                            <p class="post-card__content-desc"><?= get_the_excerpt()?></p>
                                        </div>
                                        <div class="post-card__footer">
                                            <div class="post-card__footer-author"><?= get_avatar($post->post_author,40,'',get_the_author()) ?><?php the_author() ?></div>
                                            <i class="fas fa-circle"></i>
                                            <div class="post-card__footer-date"><?php the_date() ?></div>
                                        </div>
                                    </div>
                            <?php
                            endwhile;
                        else :
                            echo 'مطلبی برای نمایش پیدا نشد!';
                        endif;
                        ?>
                    </div>
                    <!-- /main-column -->
                    <div class="pagination">
                        <?php echo paginate_links(); ?>
                    </div>
                </article>
            <!-- /site-content -->
            <?php get_sidebar(); ?>
        </div>
        <!-- /container -->
    </section>


</div>

<?php get_footer(); ?>
