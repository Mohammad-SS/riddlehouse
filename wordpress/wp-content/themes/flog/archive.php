<?php
get_header();
?>


<div class="container">

    <div class="category-main d-flex flex-column">
        <div class="category-main__top col-17">
            <div class="category-main__top-breadcrumb">
                <?php
                if ( function_exists( 'yoast_breadcrumb' ) ) {
                    yoast_breadcrumb();
                }
                ?>
            </div>
            <div class="category-main__top-subject d-flex align-items-center mb-3">
                <h1>آرشیو: </h1>
                <h1 class="page-title"> <?= single_cat_title() ?></h1>
            </div>
            <div class="category-main__top-desc"><p><?= category_description() ?>
                </p></div>
        </div>
        <div class="d-flex justify-content-between align-items-flex-start main-content mt-5 mb-5">
            <article class="category-main__content">
                <section class="category-main__content-posts d-flex flex-wrap">
                    <?php if ( have_posts() ) {
                        while ( have_posts() ) {
                            the_post();
                            $post_categories = get_the_terms( get_the_ID(), 'category' );
                            ?>
                            <div class="post-card" data-aos="fade-up" data-aos-duration="1000">
                                <div class="post-card__img"><a href="<?php the_permalink(); ?>"><?php the_thumbnail('post-card-cat') ?></a></div>
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
                        <?php }
                    } ?>
                </section>
                <div class="category-main__pagination pagination">
                    <?php echo paginate_links(); ?>
                </div>
            </article>
            <aside class="category-main__sidebar col-lg-7 me-4">
                <?php if ( is_active_sidebar( 'main-sidebar' ) ) : ?>
                    <ul id="main-sidebar">
                        <?php dynamic_sidebar( 'main-sidebar' ); ?>
                    </ul>
                <?php endif; ?>
            </aside>
        </div>
    </div>
</div>

<?php get_footer(); ?>
