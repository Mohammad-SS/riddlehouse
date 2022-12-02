<?php
if (post_password_required()) {
	return;
}
$postId = get_the_ID();
$post = get_post($postId, 'OBJECT');
setup_postdata($post);
$args = array(
	'post_id' => $postId,
);
$comments = get_comments($args);
if (!empty($_SERVER['SCRIPT_FILENAME']) && 'comments.php' == basename($_SERVER['SCRIPT_FILENAME'])) {
	die ('لطفا این صفحه را بارگزاری نکنید . متشکرم!');
}

?>

<?php if($comments){ ?>
	<div class="comment-sec">
		<div class="container">
			<div class="comment-sec__sec-ttl">
				<h5>
					دیدگاه کاربران
				</h5>
				<span class="comment-sec__comment-count">
                    <span><?= get_comments_number(get_the_ID()) ?></span>
					دیدگاه
				</span>
			</div>

			<div class="comment__lists">
				<ul>

					<?php
					wp_list_comments('type=comment&callback=better_comments',$comments);
                    ?>
				</ul>
			</div>
		</div>
	</div>
<?php } ?>
<!--comment-form-->
<?php get_template_part('comments_form'); ?>
