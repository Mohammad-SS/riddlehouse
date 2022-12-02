<header id="full-width-header"
        class="full-width-header">
	<div class="container">
		<div class="header__right d-flex flex-row align-items-center">

			<!--toggle mega-menu-responsive-->
			<div class="mega-menu-responsive">
				<i class="fas fa-bars"></i>
			</div>
			<!--end toggle mega-menu-responsive-->
			<?php 
		
			?>
			<a href="<?= get_site_url() ?>"><img src="<?= $headerLogo['url'] ?>"
			                                     alt="<?= $headerLogo['title'] ?>"></a>
		</div>
		<div class="header__center"><?php
			wp_nav_menu( array(
				'theme_location'  => 'header-menu',
				'menu_class'      => 'header_menu',
				'container'       => 'nav',
				'container_class' => 'container_header_menu',
			) );
			?></div>
		<div class="header__left">
			<div class="header__left-social">
				<?php if ( $social ) {
					foreach ( $social as $item ) {
						?>
						<a href="<?= $item["link_social"] ?>"><i class="<?= $item["icon_social"] ?>"></i></a>
						<?php
					}
				}
				?>

			</div>
			<div class="header__left-search">
				<span><i class="far fa-search"></i></span>
			</div>
		</div>
	</div>
	<div class="container search-form">
		<form action="/">
			<input type="text" name="s" placeholder="دنبال چی میگردی؟"><button type="submit">جستجو کن!</button>
		</form>
	</div>

</header>