<?php get_header(); ?>

<main class="single-post">
	<?php
	while ( have_posts() ) :
		the_post();
		?>
		
		<header class="single-header">
			<div class="container">
				<?php
				$categories = get_the_category();
				if ( ! empty( $categories ) ) {
					echo '<span class="single-category">' . esc_html( $categories[0]->name ) . '</span>';
				}
				?>
				<h1 class="single-title"><?php the_title(); ?></h1>
				<div class="single-meta">
					<span>Publicado el <?php echo get_the_date(); ?></span>
					<span style="margin: 0 10px;">|</span>
					<span>Por Sergio Ávila</span>
				</div>
			</div>
		</header>

		<?php if ( has_post_thumbnail() ) : ?>
			<div class="container">
				<div class="single-thumb">
					<?php the_post_thumbnail('full'); ?>
				</div>
			</div>
		<?php endif; ?>

		<div class="container">
			<div class="single-content">
				<?php the_content(); ?>
				
				<!-- Share or tags could go here -->
				<div style="margin-top: 4rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1);">
					<?php the_tags('<span style="color:var(--accent-gold); font-weight:bold; margin-right:10px;">Etiquetas:</span> ', ', ', ''); ?>
				</div>
			</div>
		</div>

	<?php
	endwhile;
	?>
</main>

<?php get_footer(); ?>
