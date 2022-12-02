<!--start menu-responsive-->
<div class="mega-menu-site-responsive">
	<div class="mega-menu-site-responsive__head">
		<div class="mega-menu-site-responsive__header">
            <a href="<?= get_site_url() ?>"><img src="<?= $headerLogo['sizes']['header-logo'] ?>"
                                                 alt="<?= $headerLogo['title'] ?>"></a>
			<i class="close fal fa-times-circle"></i>
		</div>

		<form action="/" class="search-header">
			<input type="text" name="s" placeholder="جستجو کنید + Enter" autocomplete="off">
		</form>
	</div>
	<div class="mega-menu-site-responsive__body" id="res-menu-body">
        <?php
        wp_nav_menu( array(
                'theme_location'  => 'header-menu',
                'menu_class'      => 'header_menu',
                'container'       => 'nav',
                'container_class' => 'container_header_menu',
        ) );
        ?>
	</div>
</div>
<!--end menu-responsive-->
