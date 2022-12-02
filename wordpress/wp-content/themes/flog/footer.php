<?php
//get variables
$subscribe_status  = get_field( 'subscribe_status', 'options' );
$subscribe_title   = get_field( 'subscribe_title', 'options' );
$subscribe_desc    = get_field( 'subscribe_desc', 'options' );
$subscribe_socials = get_field( 'subscribe_socials', 'options' );
$copyright_footer  = get_field( 'copyright_footer', 'options' );
$dev_theme         = get_field( 'dev_theme', 'options' );
?>
<footer id="footer">
    <?php if ( $subscribe_status && shortcode_exists( 'newsletter' )) { ?>
        <div class="footer__top subscribe">
            <?php if ( $subscribe_title ) { ?>
                <h3 class="subscribe__title"><?= $subscribe_title ?></h3>
            <?php }
            if ( $subscribe_desc ) {
                ?>
                <span class="subscribe__desc"><?= $subscribe_desc ?></span>
            <?php }
               echo do_shortcode( "[newsletter]" );
            ?>
            <div class="subscribe__socials">
                <?php if ( $subscribe_socials ) {
                    foreach ( $subscribe_socials as $item ) {
                        ?>
                        <a href="<?= $item['subscribe_social_link'] ?>">
                            <span><?= $item['subscribe_social_title'] ?></span><i class="<?= $item['subscribe_social_icon'] ?>"></i>
                        </a>
                        <?php
                    }
                }
                ?>

            </div>
        </div>
    <?php } ?>
    <div class="footer__bottom">
        <?php if ( $copyright_footer ) { ?>
            <div class="footer__bottom-copyright"><?= $copyright_footer ?></div>
            <?php
        }
        if ( $dev_theme ) {
            ?>
            <div class="footer__bottom-devlink">
                <a href="http://omoghadasi.ir">Developed with ❤️ by Omoghadasi</a>
            </div>
            <?php
        }
        ?>
    </div>
</footer>
<?php wp_footer(); ?>
</body>
</html>
