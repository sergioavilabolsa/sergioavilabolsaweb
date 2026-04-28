<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="profile" href="https://gmpg.org/xfn/11">
	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="site-header">
	<div class="container header-inner">
		<div class="site-logo">
			<a href="<?php echo esc_url( home_url( '/' ) ); ?>">
				Sergio Ávila<span>.</span>
			</a>
		</div>
		
		<nav class="main-nav">
			<?php
			wp_nav_menu(
				array(
					'theme_location' => 'menu-1',
					'menu_id'        => 'primary-menu',
                    'fallback_cb'    => false,
				)
			);
			?>
            <!-- Fallback if no menu is set -->
            <?php if ( ! has_nav_menu( 'menu-1' ) ) : ?>
                <ul>
                    <li><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Inicio</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/blog' ) ); ?>">Análisis</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/biografia-de-sergio-avila-luengo/' ) ); ?>">Biografía</a></li>
                    <li><a href="https://www.youtube.com/c/sergioavilabolsa" target="_blank">YouTube</a></li>
                    <li><a href="#newsletter">Newsletter</a></li>
                </ul>
            <?php endif; ?>
		</nav>
	</div>
</header>
