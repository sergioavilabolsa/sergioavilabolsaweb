<?php
/**
 * Sergio Ávila Premium functions and definitions
 */

if ( ! function_exists( 'sergiopremium_setup' ) ) :
	function sergiopremium_setup() {
		// Add default posts and comments RSS feed links to head.
		add_theme_support( 'automatic-feed-links' );

		// Let WordPress manage the document title.
		add_theme_support( 'title-tag' );

		// Enable support for Post Thumbnails on posts and pages.
		add_theme_support( 'post-thumbnails' );

		// This theme uses wp_nav_menu() in one location.
		register_nav_menus(
			array(
				'menu-1' => esc_html__( 'Primary', 'sergiopremium' ),
				'footer' => esc_html__( 'Footer Menu', 'sergiopremium' ),
			)
		);

		// Switch default core markup for search form, comment form, and comments to output valid HTML5.
		add_theme_support(
			'html5',
			array(
				'search-form',
				'comment-form',
				'comment-list',
				'gallery',
				'caption',
				'style',
				'script',
			)
		);
	}
endif;
add_action( 'after_setup_theme', 'sergiopremium_setup' );

/**
 * Enqueue scripts and styles.
 */
function sergiopremium_scripts() {
	// Google Fonts
	wp_enqueue_style( 'sergiopremium-fonts', 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@400;600;700&display=swap', array(), null );
	
	// Main Style
	wp_enqueue_style( 'sergiopremium-style', get_stylesheet_uri(), array(), '1.0.0' );
}
add_action( 'wp_enqueue_scripts', 'sergiopremium_scripts' );

/**
 * Custom excerpt length for automated articles
 */
function sergiopremium_custom_excerpt_length( $length ) {
    return 20;
}
add_filter( 'excerpt_length', 'sergiopremium_custom_excerpt_length', 999 );

/**
 * Redirect legacy domain traffic to preferred domain.
 * Keeps path/query so old URLs migrate cleanly.
 */
function sergiopremium_redirect_legacy_domains() {
	if ( is_admin() || wp_doing_ajax() || wp_doing_cron() ) {
		return;
	}

	$preferred_domain = 'sergioavilabolsa.es';
	$legacy_domains   = array(
		'sergioavilabolsa.com',
		'www.sergioavilabolsa.com',
		'www.sergioavilabolsa.es',
	);

	$host = isset( $_SERVER['HTTP_HOST'] ) ? strtolower( wp_unslash( $_SERVER['HTTP_HOST'] ) ) : '';
	if ( '' === $host ) {
		return;
	}

	if ( in_array( $host, $legacy_domains, true ) ) {
		$request_uri = isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '/';
		$target_url  = 'https://' . $preferred_domain . $request_uri;
		wp_safe_redirect( $target_url, 301 );
		exit;
	}
}
add_action( 'template_redirect', 'sergiopremium_redirect_legacy_domains', 1 );

/**
 * Ensure biography page exists on the new site.
 */
function sergiopremium_ensure_biography_page() {
	$slug = 'biografia-de-sergio-avila-luengo';

	$existing_page = get_page_by_path( $slug, OBJECT, 'page' );
	if ( $existing_page ) {
		return;
	}

	$page_id = wp_insert_post(
		array(
			'post_title'   => 'Biografía de Sergio Ávila Luengo',
			'post_name'    => $slug,
			'post_type'    => 'page',
			'post_status'  => 'publish',
			'post_content' => 'Página de biografía de Sergio Ávila.',
		),
		true
	);

	if ( ! is_wp_error( $page_id ) ) {
		update_option( 'sergiopremium_biography_page_id', (int) $page_id );
	}
}
add_action( 'init', 'sergiopremium_ensure_biography_page' );
