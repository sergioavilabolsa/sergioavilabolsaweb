<?php get_header(); ?>

<main>
	<!-- Hero Section -->
	<section class="hero">
		<div class="container hero-inner">
			<div class="hero-content">
				<h1>Análisis Institucional.<br>Estrategia Real.</h1>
				<p>Soy Sergio Ávila, analista con 20 años de experiencia. Descubre el análisis de mercados sin ruido, con datos objetivos y estrategias operativas realistas para maximizar tu cartera.</p>
				<div class="hero-actions">
					<a href="#analisis" class="btn btn-primary">Últimos Análisis</a>
					<a href="https://www.youtube.com/c/sergioavilabolsa" target="_blank" class="btn btn-outline">Ver en YouTube</a>
				</div>
			</div>
			<div class="hero-image-wrapper">
				<!-- Sergio's professional photo -->
				<img src="<?php echo esc_url( get_template_directory_uri() . '/assets/images/sergio-hero.jpg' ); ?>" alt="Sergio Ávila Analista Financiero" class="hero-image" onerror="if(!this.dataset.fallback){this.dataset.fallback='1';this.src='<?php echo esc_url( get_template_directory_uri() . '/assets%5Cimages%5Csergio-hero.jpg' ); ?>';}else{this.onerror=null;this.style.opacity='0';}" style="border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
			</div>
		</div>
	</section>

	<!-- Latest Analysis Section -->
	<section id="analisis" class="latest-analysis">
		<div class="container">
			<h2 class="section-title">Análisis de <span>Mercados</span></h2>
			<div class="articles-grid">
				<?php
				// Query to get the latest 6 posts (which will include the automated AI articles)
				$args = array(
					'post_type'      => 'post',
					'posts_per_page' => 6,
					'post_status'    => 'publish'
				);
				$query = new WP_Query($args);

				if ($query->have_posts()) :
					while ($query->have_posts()) : $query->the_post();
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
					wp_reset_postdata();
				else :
					echo '<p style="text-align:center; color:var(--text-muted);">Aún no hay análisis publicados.</p>';
				endif;
				?>
			</div>
		</div>
	</section>

	<!-- About Section -->
	<section class="about-section">
		<div class="container about-inner">
			<div class="about-image">
				<img src="<?php echo esc_url( get_template_directory_uri() . '/assets/images/sergio-about.jpg' ); ?>" alt="Sergio Ávila - Top Analista IG" onerror="if(!this.dataset.fallback){this.dataset.fallback='1';this.src='<?php echo esc_url( get_template_directory_uri() . '/assets%5Cimages%5Csergio-about.jpg' ); ?>';}else{this.onerror=null;this.style.opacity='0';}" style="border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
			</div>
			<div class="about-content">
				<h2 style="font-size: 2.5rem; margin-bottom: 1.5rem;">Análisis Claro y <span style="color:var(--accent-gold);">Basado en Datos</span></h2>
				<p style="font-size: 1.1rem; color: var(--text-muted); margin-bottom: 1.5rem;">Ofrezco un análisis de mercados claro y basado en datos que ayuda a los inversores a comprender entornos financieros complejos y a tomar decisiones de inversión con criterio.</p>
				<p style="font-size: 1.1rem; color: var(--text-muted);">Mi enfoque combina la experiencia técnica con una comunicación accesible, permitiendo identificar oportunidades accionables, gestionar el riesgo de forma eficaz y comprender la psicología colectiva detrás de cada movimiento de precio.</p>
				
				<div class="about-stats">
					<div class="stat-item">
						<div class="stat-num">20+</div>
						<div class="stat-label">Años de Experiencia</div>
					</div>
					<div class="stat-item">
						<div class="stat-num">Top</div>
						<div class="stat-label">Analista en IG.com</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- Newsletter CTA -->
	<section id="newsletter" class="newsletter-cta">
		<div class="container">
			<div class="cta-box">
				<h2>La Información es Rentabilidad</h2>
				<p>Únete a mi newsletter gratuita y recibe antes que nadie los análisis clave de la semana, perspectivas de mercado y estrategias operativas exclusivas.</p>
				<!-- Replace with actual Revue/Mailchimp form code -->
				<form action="#" style="display: flex; gap: 1rem; max-width: 500px; margin: 0 auto;">
					<input type="email" placeholder="Tu mejor email..." style="flex: 1; padding: 1rem 1.5rem; border-radius: 50px; border: 1px solid rgba(255,255,255,0.2); background: rgba(0,0,0,0.5); color: #fff; outline: none;">
					<button type="submit" class="btn btn-primary">Suscribirme</button>
				</form>
				<p style="font-size: 0.8rem; margin-top: 1rem; opacity: 0.7;">100% libre de spam. Puedes darte de baja cuando quieras.</p>
			</div>
		</div>
	</section>

</main>

<?php get_footer(); ?>
