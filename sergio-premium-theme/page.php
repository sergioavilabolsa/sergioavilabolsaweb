<?php get_header(); ?>

<main class="container" style="padding: 4rem 2rem;">
	<?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
		<article class="single-content" style="max-width: 900px;">
			<header style="margin-bottom: 2rem; text-align: center;">
				<h1 class="single-title" style="margin-bottom: 0.5rem;"><?php the_title(); ?></h1>
			</header>
			<div class="entry-content">
				<?php the_content(); ?>
			</div>
		</article>
	<?php endwhile; endif; ?>
</main>

<?php get_footer(); ?>
