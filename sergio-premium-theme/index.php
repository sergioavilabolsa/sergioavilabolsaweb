<?php get_header(); ?>

<main class="container" style="padding: 4rem 2rem;">
	<h1 class="section-title">Análisis del <span>Mercado</span></h1>
	
	<div class="articles-grid">
		<?php
		if ( have_posts() ) :
			while ( have_posts() ) : the_post();
		?>
				<article class="article-card">
					<div class="article-thumb">
						<a href="<?php the_permalink(); ?>">
							<?php 
							if ( has_post_thumbnail() ) {
								the_post_thumbnail('medium_large');
							} else {
								echo '<div style="width: 100%; height: 200px; background: linear-gradient(135deg, var(--bg-darker) 0%, #1a1e29 100%); display: flex; align-items: center; justify-content: center;"><span style="color: rgba(255, 255, 255, 0.1); font-size: 4rem; font-weight: 800; letter-spacing: -2px;">SÁ.</span></div>';
							}
							?>
						</a>
					</div>
					<div class="article-content">
						<?php
						$categories = get_the_category();
						if ( ! empty( $categories ) ) {
							echo '<span class="article-meta">' . esc_html( $categories[0]->name ) . '</span>';
						}
						?>
						<h3 class="article-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
						<div class="article-excerpt">
							<?php echo wp_trim_words( get_the_excerpt(), 20, '...' ); ?>
						</div>
						<a href="<?php the_permalink(); ?>" style="font-weight: 600; font-size: 0.9rem;">Leer Análisis &rarr;</a>
					</div>
				</article>
		<?php
			endwhile;
			
			// Pagination
			the_posts_pagination( array(
				'prev_text' => '&larr; Anteriores',
				'next_text' => 'Siguientes &rarr;',
			) );

		else :
			echo '<p>No se encontraron artículos.</p>';
		endif;
		?>
	</div>
</main>

<?php get_footer(); ?>
