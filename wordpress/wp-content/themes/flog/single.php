<?php
get_header();
?>
<div class="single-container container">
    <div class="spacer"></div>
    <div class="single-main d-flex justify-content-between align-items-flex-start main-content">
        <article class="single-main__content">
            <section class="single-main__content-posts d-flex flex-wrap">
                <?php if ( have_posts() ) {
                    $next            = get_next_post();
                    $hasNextPost     = get_next_post( $next );
                    $nextPostLink    = get_permalink( $next );
                    $nextPostTitle   = get_the_title( $next );

                    $prev            = get_previous_post();
                    $hasPrevPost     = get_previous_post( $prev );
                    $prevPostLink    = get_permalink( $prev );
                    $prevPostTitle   = get_the_title( $prev );

                    $post_categories = get_the_terms( get_the_ID(), 'category' );
                    ?>
                    <div class="post-card"
                         data-aos="fade-up"
                         data-aos-duration="1000">
                        <div class="post-card__img">
                            <a href="<?php the_permalink(); ?>"><?php the_thumbnail( 'post-card-single' ) ?></a></div>
                        <div class="post-card__content">
                            <div class="post-card__content-categories">
                                <?php
                                foreach ( $post_categories as $cat ) {
                                    echo '<a href="' . get_term_link( $cat->term_id ) . '" class="post-cat"><h4>' . __( $cat->name ) . '</h4></a>';
                                } ?>
                            </div>
                            <h1 class="post-card__content-title">
                                <a href="<?php the_permalink() ?>"><?php the_title() ?></a></h1>
                            <div class="post-card__information">
                                <div class="post-card__information-author"><?= get_avatar( $post->post_author, 40, '', get_the_author() ) ?><?php the_author() ?></div>
                                <i class="fas fa-circle"></i>
                                <div class="post-card__information-date"><?php the_date() ?></div>
                                <i class="fas fa-circle"></i>
                                <div class="post-card__information-comment"><?= get_comments_number( get_the_ID() ) . ' دیدگاه' ?></div>
                            </div>
                            <?php the_content() ?>
                        </div>
                        <div class="post-card__footer">
                            <div class="post-card__footer-tags">
                                <ul><?php
                                    if ( get_the_tags( get_the_ID() ) ) {
                                        foreach ( get_the_tags( get_the_ID() ) as $tag ) {
                                            ?>
                                            <li><a href="<?= get_tag_link( $tag ) ?>"><?= $tag->name ?></a></li>
                                        <?php }
                                    } ?>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <!--                next and prev post-->
                    <div class="navigation-post d-flex align-items-center justify-content-between w-100">
                        <?php if ($hasPrevPost){ ?>
                        <div class="navigation-post__prev">
                            <div class="d-flex align-items-center justify-content-between content">
                                <div class="text-left text">
                                    <div class="text-top justify-content-end"><a href="<?= $prevPostLink ?>"><i class="far fa-long-arrow-alt-right"></i>نوشته قبلی</a></div>
                                    <div class="text-bottom"><a href="<?= $prevPostLink ?>"><?= $prevPostTitle ?></a></div>
                                </div>
                                <div class="img"><?php the_thumbnail( 'post-card-small',null,$prev) ?>
                                </div>
                            </div>
                        </div>
                        <?php }
                        if ($hasNextPost){?>
                        <div class="navigation-post__next">
                            <div class="d-flex align-items-center justify-content-between content">
                                <div class="img"><?php the_thumbnail( 'post-card-small',null,$next) ?></div>
                                <div class="text-right text">
                                    <div class="text-top"><a href="<?= $nextPostLink ?>">نوشته بعدی<i class="far fa-long-arrow-alt-left"></i></a></div>
                                    <div class="text-bottom"><a href="<?= $nextPostLink ?>"><?= $nextPostTitle ?></a></div>
                                </div>
                            </div>
                        </div>
                        <?php } ?>
                    </div>

                        <!--comments-list-->
                        <?php
                        if ( comments_open() || get_comments_number() ) {
                            comments_template();
                        }
                        ?>
                        <?php } ?>

            </section>
        </article>
        <aside class="single-main__sidebar col-lg-7 me-4">
            <div class="single-main__sidebar-author">
                <?= get_avatar(get_the_author()); ?>
                <h3><?= get_the_author() ?></h3>
                <p><?= get_the_author_meta('description',get_the_author_ID()) ?></p>
            </div>
            <?php if ( is_active_sidebar( 'main-sidebar' ) ) : ?>
                <ul id="main-sidebar">
                    <?php dynamic_sidebar( 'main-sidebar' ); ?>
                </ul>
            <?php endif; ?>
        </aside>
    </div>
</div>
<?php get_footer(); ?>
