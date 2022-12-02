<?php
get_header();
?>


<div class="container">

    <div class="page-main d-flex flex-column">
        <div class="page-main__top col-17">
            <div class="page-main__top-breadcrumb">
                <?php
                if ( function_exists( 'yoast_breadcrumb' ) ) {
                    yoast_breadcrumb();
                }
                ?>
            </div>
            <div class="page-main__top-subject d-flex align-items-center mb-3">
                <h1 class="page-title"> <?= get_the_title() ?></h1>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-flex-start main-content">
            <article class="page-main__content">
                   <?php the_content(); ?>
            </article>
            <aside class="page-main__sidebar col-lg-7 me-4">
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
