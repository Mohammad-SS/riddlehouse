<!-- comment-form-->
<?php
if (comments_open()) {
	?>
	<div class="container">
		<div class="form">
			<form action="<?= SITE_URL ?>/wp-comments-post.php" class="form" method="post" id="respond">
				<div class="form__title">
					<div class="form__title-right">
						<i class="icon-Post_a_comment"></i>
						ارسال دیدگاه
					</div>

					<?php if (is_user_logged_in()==false): ?>
						<a href="/login"
						   title="">وارد حساب کاربری شوید</a>
					<?php endif; ?>
				</div>
				<?php
				$comment_name = null;
				$comment_email = null;
				if (is_user_logged_in()) {
					$user = wp_get_current_user();
					$comment_name = $user->user_nicename;
					$comment_email = $user->user_email;

				}
				comment_id_fields();
				do_action('comment_form', $post->ID);
				?>
				<div class="form__textarea">
					<i class="icon-Profile-image-icon"></i>
					<textarea name="comment" placeholder="دیدگاه خود را اینجا وارد کنید"></textarea>

				</div>
				<div class="form__footer">
					<?php if(is_user_logged_in()==false){ ?>
						<div class="form__inputs">
							<div class="form__input">
								<input type="text" name="author" placeholder="نام شما" <?= $comment_name ? 'value="' . $comment_name . '" readonly' : '' ?>>
							</div>
							<div class="form__input">
								<input type="email" name="email" placeholder="ایمیل شما" <?= $comment_email ? 'value="' . $comment_email . '" readonly' : '' ?>>
							</div>

						</div>
					<?php } ?>
					<div class="form__button">
						<button>ارسال</button>
					</div>

				</div>

			</form>
		</div>

	</div>
	<?php
}
?>
