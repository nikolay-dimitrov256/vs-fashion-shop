/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header
3. Init Menu
4. Init Thumbnail
5. Init Quantity
6. Init Star Rating
7. Init Favorite
8. Init Tabs



******************************/

jQuery(document).ready(function($)
{
	"use strict";

	/* 

	1. Vars and Inits

	*/

	var header = $('.header');
	var topNav = $('.top_nav')
	var hamburger = $('.hamburger_container');
	var menu = $('.hamburger_menu');
	var menuActive = false;
	var hamburgerClose = $('.hamburger_close');
	var fsOverlay = $('.fs_menu_overlay');
	const sizesDivElement = document.querySelector('.sizes');

	setHeader();

	$(window).on('resize', function()
	{
		setHeader();
	});

	$(document).on('scroll', function()
	{
		setHeader();
	});

	initMenu();
	initThumbnail();
	initQuantity();
	initStarRating();
	initFavorite();
	initTabs();
	initSizes();
	initFavoriteColors();
	initSlider();
	InitAddToCart();
	initReviewForm();

	/*

	Set Sizes

	*/
	
	function initSizes() {
		const sizesElements = sizesDivElement.querySelectorAll('.size');
		sizesElements.forEach(sizeElement => sizeElement.addEventListener('click', () => {
			sizesElements.forEach(element => element.classList.remove('selected'));
			sizeElement.classList.add('selected');
		}));
	}

	/* 

	2. Set Header

	*/

	function setHeader()
	{
		if(window.innerWidth < 992)
		{
			if($(window).scrollTop() > 100)
			{
				header.css({'top':"0"});
			}
			else
			{
				header.css({'top':"0"});
			}
		}
		else
		{
			if($(window).scrollTop() > 100)
			{
				header.css({'top':"-50px"});
			}
			else
			{
				header.css({'top':"0"});
			}
		}
		if(window.innerWidth > 991 && menuActive)
		{
			closeMenu();
		}
	}

	/* 

	3. Init Menu

	*/

	function initMenu()
	{
		if(hamburger.length)
		{
			hamburger.on('click', function()
			{
				if(!menuActive)
				{
					openMenu();
				}
			});
		}

		if(fsOverlay.length)
		{
			fsOverlay.on('click', function()
			{
				if(menuActive)
				{
					closeMenu();
				}
			});
		}

		if(hamburgerClose.length)
		{
			hamburgerClose.on('click', function()
			{
				if(menuActive)
				{
					closeMenu();
				}
			});
		}

		if($('.menu_item').length)
		{
			var items = document.getElementsByClassName('menu_item');
			var i;

			for(i = 0; i < items.length; i++)
			{
				if(items[i].classList.contains("has-children"))
				{
					items[i].onclick = function()
					{
						this.classList.toggle("active");
						var panel = this.children[1];
					    if(panel.style.maxHeight)
					    {
					    	panel.style.maxHeight = null;
					    }
					    else
					    {
					    	panel.style.maxHeight = panel.scrollHeight + "px";
					    }
					}
				}	
			}
		}
	}

	function openMenu()
	{
		menu.addClass('active');
		// menu.css('right', "0");
		fsOverlay.css('pointer-events', "auto");
		menuActive = true;
	}

	function closeMenu()
	{
		menu.removeClass('active');
		fsOverlay.css('pointer-events', "none");
		menuActive = false;
	}

	/* 

	4. Init Thumbnail

	*/

	// function initThumbnail()
	// {
	// 	if($('.single_product_thumbnails ul li').length)
	// 	{
	// 		var thumbs = $('.single_product_thumbnails ul li');
	// 		var singleImage = $('.single_product_image_background');

	// 		thumbs.each(function()
	// 		{
	// 			var item = $(this);
	// 			item.on('click', function()
	// 			{
	// 				thumbs.removeClass('active');
	// 				item.addClass('active');
	// 				var img = item.find('img').data('image');
	// 				singleImage.css('background-image', 'url(' + img + ')');
	// 			});
	// 		});
	// 	}	
	// }

	function initThumbnail() {
		const thumbnails = document.querySelectorAll('.single_product_thumbnails ul li');
		const focusImage = document.querySelector('.single_product_image img');
		
		if (!thumbnails.length) {
			return;
		}

		thumbnails.forEach(thumb => thumb.addEventListener('click', () => {
			thumbnails.forEach(thumbnail => thumbnail.classList.remove('active'));
			thumb.classList.add('active');
			focusImage.src = thumb.querySelector('img').src;
		}));
	}

	/* 

	5. Init Quantity

	*/

	function initQuantity()
	{
		if($('.plus').length && $('.minus').length)
		{
			var plus = $('.plus');
			var minus = $('.minus');
			var value = $('#quantity_value');

			plus.on('click', function()
			{
				var x = parseInt(value.text());
				value.text(x + 1);
			});

			minus.on('click', function()
			{
				var x = parseInt(value.text());
				if(x > 1)
				{
					value.text(x - 1);
				}
			});
		}
	}

	/* 

	6. Init Star Rating

	*/

	function initStarRating()
	{
		if($('.user_star_rating li').length)
		{
			var stars = $('.user_star_rating li');

			stars.each(function()
			{
				var star = $(this);

				star.on('click', function()
				{
					var i = star.index();

					stars.find('i').each(function()
					{
						$(this).removeClass('fa-star');
						$(this).addClass('fa-star-o');
					});
					for(var x = 0; x <= i; x++)
					{
						$(stars[x]).find('i').removeClass('fa-star-o');
						$(stars[x]).find('i').addClass('fa-star');
					};

					// Set the rating in the hidden input
					$('#id_rating').val(i + 1);
				});

				// Hover effect
				star.on('mouseenter', function () {
					const index = $(this).index();

					stars.each(function (i) {
						const icon = $(this).find('i');
						if (i <= index) {
							icon.removeClass('fa-star-o').addClass('fa-star');
						} else {
							icon.removeClass('fa-star').addClass('fa-star-o');
						}
					});
				});

				// Hover out: restore selected rating
				star.on('mouseleave', function () {
					var selected = $('#id_rating').val();

					stars.find('i').removeClass('fa-star').addClass('fa-star-o');
					for (var x = 0; x < selected; x++) {
						$(stars[x]).find('i').removeClass('fa-star-o').addClass('fa-star');
					}
				});
			});
		}
	}

	/* 

	7. Init Favorite

	*/

	function initFavorite()
	{
		if($('.product_favorite').length)
		{
			var fav = $('.product_favorite');

			fav.on('click', function()
			{
				fav.toggleClass('active');
			});
		}
	}

	/* 

	8. Init Tabs

	*/

	function initTabs()
	{
		if($('.tabs').length)
		{
			var tabs = $('.tabs li');
			var tabContainers = $('.tab_container');

			tabs.each(function()
			{
				var tab = $(this);
				var tab_id = tab.data('active-tab');

				tab.on('click', function()
				{
					if(!tab.hasClass('active'))
					{
						tabs.removeClass('active');
						tabContainers.removeClass('active');
						tab.addClass('active');
						$('#' + tab_id).addClass('active');
					}
				});
			});
		}
	}

	/* 

	9. Init Favorite

	*/

	function initFavoriteColors()
    {
    	if($('.favorite').length)
    	{
    		var favs = $('.favorite');

    		favs.each(function()
    		{
    			var fav = $(this);
    			var active = false;
    			if(fav.hasClass('active'))
    			{
    				active = true;
    			}

    			fav.on('click', function()
    			{
    				if(active)
    				{
    					fav.removeClass('active');
    					active = false;
    				}
    				else
    				{
    					fav.addClass('active');
    					active = true;
    				}
    			});
    		});
    	}
    }

	/* 

	10. Init Slider

	*/

    function initSlider()
    {
    	if($('.product_slider').length)
    	{
    		var slider1 = $('.product_slider');

    		slider1.owlCarousel({
    			loop:false,
    			dots:false,
    			nav:false,
    			responsive:
				{
					0:{items:1},
					480:{items:2},
					768:{items:3},
					991:{items:4},
					1280:{items:5},
					1440:{items:5}
				}
    		});

    		if($('.product_slider_nav_left').length)
    		{
    			$('.product_slider_nav_left').on('click', function()
    			{
    				slider1.trigger('prev.owl.carousel');
    			});
    		}

    		if($('.product_slider_nav_right').length)
    		{
    			$('.product_slider_nav_right').on('click', function()
    			{
    				slider1.trigger('next.owl.carousel');
    			});
    		}
    	}
    }

	function InitAddToCart() {
		const addFormElement = document.getElementById('add-form');
		const addToCartButtonAElement = document.querySelector('.add_to_cart_button a');
		const sizesDivElement = document.querySelector('.sizes');
		const quantitySpanElement = document.getElementById('quantity_value');
		const sizeHiddenInputElement = document.getElementById('size');
		const quantityHiddenInputElement = document.getElementById('quantity');
		const allSizesElements = sizesDivElement.querySelectorAll('.size');

		addToCartButtonAElement.addEventListener('click', (e)=>{
			e.preventDefault();

			// If there is only one size, add it to cart without making the user click it
			if (allSizesElements.length == 1) {
				allSizesElements[0].classList.add('selected');
			}

			const sizeDivElement = sizesDivElement.querySelector('.selected');
			const quantity = quantitySpanElement.textContent;
			
			if (!sizeDivElement) {
				alert('Моля изберете размер.');
				return;
			}
			
			const size = sizeDivElement.textContent;
			sizeHiddenInputElement.value = size;
			quantityHiddenInputElement.value = quantity;

			addFormElement.submit();
		})
	}

	function initReviewForm() {
		const form = document.getElementById('review_form');
		const submitButtonElement = document.getElementById('review_submit');


		submitButtonElement.addEventListener('click', (e) => {
			e.preventDefault();
			const author = document.getElementById('id_author').value.trim();
			const rating = document.getElementById('id_rating').value;
			const content = document.getElementById('id_content').value.trim();
			
			if (!rating) {
				alert('Моля изберете своята оценка.');
				return;
			} else if (!author) {
				alert('Моля напишете имената си.');
				return;
			} else if (!content || content.length <5) {
				alert('Моля напишете своя отзив.');
				return;
			}

			submitButtonElement.disabled = true;
			form.submit();
		});
	}
});