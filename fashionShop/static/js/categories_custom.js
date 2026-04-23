/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header
3. Init Menu
4. Init Favorite
5. Init Fix Product Border
6. Init Isotope Filtering
7. Init Price Slider
8. Init Checkboxes



******************************/

jQuery(document).ready(function($)
{
	"use strict";

	/* 

	1. Vars and Inits

	*/

	var header = $('.header');
	var topNav = $('.top_nav')
	var mainSlider = $('.main_slider');
	var hamburger = $('.hamburger_container');
	var menu = $('.hamburger_menu');
	var menuActive = false;
	var hamburgerClose = $('.hamburger_close');
	var fsOverlay = $('.fs_menu_overlay');
	const fetchParams = JSON.parse(document.getElementById('fetch-params').textContent);
	const translations = JSON.parse(document.getElementById('translations').textContent);
	let allContentIsLoaded = !fetchParams.next;
	let isLoading = false;

	setHeader();

	$(window).on('resize', function()
	{
		initFixProductBorder();
		setHeader();
		//rearangeSidebar();
		initFilters();
	});

	$(document).on('scroll', function()
	{
		setHeader();

		const loadItems = evaluatePosition();
		
		if (loadItems && !allContentIsLoaded && !isLoading) {
			loadContent();
		}
	});

	//rearangeSidebar();
	initFilters();
	initMenu();
	initFavorite();
	// initFixProductBorder();
	// initIsotopeFiltering();
	// initIsotopeLayoutOnly();
	// initPriceSlider();
	initCheckboxes();
	initPagination();

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

	4. Init Favorite

	*/

    function initFavorite()
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

	5. Init Fix Product Border

	*/

    function initFixProductBorder()
    {
    	if($('.product_filter').length)
    	{
			var products = $('.product_filter:visible');
    		var wdth = window.innerWidth;

    		// reset border
    		products.each(function()
    		{
    			$(this).css('border-right', 'solid 1px #e9e9e9');
    		});

    		// if window width is 991px or less

    		if(wdth < 480)
			{
				for(var i = 0; i < products.length; i++)
				{
					var product = $(products[i]);
					product.css('border-right', 'none');
				}
			}

    		else if(wdth < 576)
			{
				if(products.length < 5)
				{
					var product = $(products[products.length - 1]);
					product.css('border-right', 'none');
				}
				for(var i = 1; i < products.length; i+=2)
				{
					var product = $(products[i]);
					product.css('border-right', 'none');
				}
			}

    		else if(wdth < 768)
			{
				if(products.length < 5)
				{
					var product = $(products[products.length - 1]);
					product.css('border-right', 'none');
				}
				for(var i = 2; i < products.length; i+=3)
				{
					var product = $(products[i]);
					product.css('border-right', 'none');
				}
			}

    		else if(wdth < 992)
			{
				if(products.length < 5)
				{
					var product = $(products[products.length - 1]);
					product.css('border-right', 'none');
				}
				for(var i = 2; i < products.length; i+=3)
				{
					var product = $(products[i]);
					product.css('border-right', 'none');
				}
			}

			//if window width is larger than 991px
			else
			{
				if(products.length < 5)
				{
					var product = $(products[products.length - 1]);
					product.css('border-right', 'none');
				}
				for(var i = 3; i < products.length; i+=4)
				{
					var product = $(products[i]);
					product.css('border-right', 'none');
				}
			}	
    	}
    }

    /* 

	6. Init Isotope Filtering

	*/

    function initIsotopeFiltering()
    {
    	var sortTypes = $('.type_sorting_btn');
    	var sortNums = $('.num_sorting_btn');
    	var sortTypesSelected = $('.sorting_type .item_sorting_btn is-checked span');
    	var filterButton = $('.filter_button');

    	if($('.product-grid').length)
    	{
    		$('.product-grid').isotope({
    			itemSelector: '.product-item',
	            getSortData: {
	            	price: function(itemElement)
	            	{
	            		var priceEle = $(itemElement).find('.product_price').text().replace( '$', '' );
	            		return parseFloat(priceEle);
	            	},
	            	name: '.product_name'
	            },
	            animationOptions: {
	                duration: 750,
	                easing: 'linear',
	                queue: false
	            }
	        });

    		// Short based on the value from the sorting_type dropdown
	        sortTypes.each(function()
	        {
	        	$(this).on('click', function()
	        	{
	        		$('.type_sorting_text').text($(this).text());
	        		var option = $(this).attr('data-isotope-option');
	        		option = JSON.parse( option );
    				$('.product-grid').isotope( option );
	        	});
	        });

	        // Show only a selected number of items
	        // sortNums.each(function()
	        // {
	        // 	$(this).on('click', function()
	        // 	{
	        // 		var numSortingText = $(this).text();
			// 		var numFilter = ':nth-child(-n+' + numSortingText + ')';
	        // 		$('.num_sorting_text').text($(this).text());
    		// 		$('.product-grid').isotope({filter: numFilter });
	        // 	});
	        // });	

	        // Filter based on the price range slider
	        filterButton.on('click', function()
	        {
	        	$('.product-grid').isotope({
		            filter: function()
		            {
		            	var priceRange = $('#amount').val();
			        	var priceMin = parseFloat(priceRange.split('-')[0].replace('$', ''));
			        	var priceMax = parseFloat(priceRange.split('-')[1].replace('$', ''));
			        	var itemPrice = $(this).find('.product_price').clone().children().remove().end().text().replace( '$', '' );

			        	return (itemPrice > priceMin) && (itemPrice < priceMax);
		            },
		            animationOptions: {
		                duration: 750,
		                easing: 'linear',
		                queue: false
		            }
		        });
	        });
    	}
    }

    /* 

	7. Init Price Slider

	*/

    function initPriceSlider()
    {
		$( "#slider-range" ).slider(
		{
			range: true,
			min: 0,
			max: 1000,
			values: [ 0, 580 ],
			slide: function( event, ui )
			{
				$( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
			}
		});
			
		$( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) + " - $" + $( "#slider-range" ).slider( "values", 1 ) );
    }

    /* 

	8. Init Checkboxes

	*/

    function initCheckboxes()
    {
		const filterForms = document.querySelectorAll('.filter_form');
		filterForms.forEach(form => {
			const showToggleElement = form.querySelector('.show_toggle');
			const showMoreDivElement = form.querySelector('.show_more');
			const showLessHiddenDivElement = form.querySelector('.show_less');

			showToggleElement.addEventListener('click', ()=>{
				const spanElementToHide = showMoreDivElement.querySelector('span');
				const spanElementToShow = showLessHiddenDivElement.querySelector('span');

				showMoreDivElement.append(spanElementToShow);
				showLessHiddenDivElement.append(spanElementToHide);
			});
		});
    }

	function initPagination() {
		const paginationFormElement = document.getElementById('pagination_form');
		const paginateByInputElement = document.getElementById('paginate_by');
		const selectPagesLiElements = document.querySelectorAll('.num_sorting_btn');

		selectPagesLiElements.forEach(element => {
			element.addEventListener('click', () => {
				let paginateBy = element.querySelector('span').textContent;
				paginateByInputElement.value = paginateBy;
				paginationFormElement.submit();
			});
		});
	}

	function initIsotopeLayoutOnly() {
		if ($('.product-grid').length) {
			var $grid = $('.product-grid');
	
			// Initialize Isotope first (so layout mode is known)
			$grid.isotope({
				itemSelector: '.product-item',
				layoutMode: 'fitRows', // or 'masonry'
				animationOptions: {
					duration: 750,
					easing: 'linear',
					queue: false
				}
			});
	
			// Then trigger layout only *after* images are loaded
			$grid.imagesLoaded().progress(function () {
				$grid.isotope('layout');
			});
		}
	}
	
	function rearangeSidebar() {
		// Get elements
		const parentDivElement = document.querySelector('.product_section');
		const sidebarDivElement = document.querySelector('.sidebar');
		const contentDivElement = document.querySelector('.main_content');

		if (window.innerWidth <= 991) {
			parentDivElement.append(sidebarDivElement);
		} else {
			parentDivElement.insertBefore(sidebarDivElement, contentDivElement);
		}
	}

	function initFilters() {
		const sidebarDivElement = document.querySelector('.sidebar');
		const filterDivElements = sidebarDivElement.querySelectorAll('.sidebar_section');
		const filterAElements = sidebarDivElement.querySelectorAll('.filter-button');

		if (window.innerWidth <= 991) {
			filterAElements.forEach(element => {
				element.style.display = 'inline-block';
			});

			filterDivElements.forEach(element => {
			element.style.display = 'none';
			
			// Expand filter parameters
			const toggleInputElement = element.querySelector('.show_toggle');
			toggleInputElement.checked = true;
			// Hide labels
			const showLabelElement = element.querySelector('label.show_more');
			showLabelElement.style.display = 'none';
		});
		} else {
			filterAElements.forEach(element => {
				element.style.display = 'none';
			});

			filterDivElements.forEach(element => {
				element.style.display = 'block';

				// Colapse filter parameters
				const toggleInputElement = element.querySelector('.show_toggle');
				toggleInputElement.checked = false;
				// Show labels
				const showLabelElement = element.querySelector('label.show_more');
				showLabelElement.style.display = 'block';
			});
		}
		
		filterAElements.forEach(element => {
			element.addEventListener('click', e => toggleFilters(e, element));
		});
	}

	function toggleFilters(e, element) {
		e.preventDefault();
		const filterDivElement = element.nextElementSibling;
		filterDivElement.style.display = 'block';
		element.style.display = 'none';
	}

	function evaluatePosition() {
		// Get scroll values
		const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
		// Get elements
		const footerElement = document.querySelector('footer.footer');
		const bottomArticleElement = document.querySelector('.bottom-article');
		const benefitElement = document.querySelector('.benefit');
		const itemCardElement = document.querySelector('.product-item');

		// Get elements heights
		const footerHeight = getElementHeight(footerElement);
		const bottomArticleHeight = getElementHeight(bottomArticleElement);
		const benefitHeight = getElementHeight(benefitElement);
		const itemCardHeight = getElementHeight(itemCardElement);
		
		// The bottom of the screen is two rows away from the end of content
		return scrollTop + clientHeight >= scrollHeight - (footerHeight + bottomArticleHeight + benefitHeight + itemCardHeight * 2);
	}

	function getElementHeight(element) {
		if (!element) {
			return 0;
		}
		const styles = getComputedStyle(element)
		const height = element.getBoundingClientRect().height + parseFloat(styles.marginTop) + parseFloat(styles.marginBottom);

		return height;
	}

	function loadContent() {
		isLoading = true;
		
		// Fetch data
		fetch(fetchParams.next)
		.then(res => res.json())
		.then(data => {
			renderItems(data.results);
			fetchParams.next = data.next;
			fetchParams.previous = data.previous;

			if (!data.next) {
				allContentIsLoaded = true;
			}
		})
		.catch(error => console.error(error))
		.finally(() => { isLoading = false; })
	}

	function renderItems(items) {
		const productGridElement = document.querySelector('.product-grid');
		const cards = [];

		for (const item of items) {
			const card = makeCard(item);
			cards.push(card);
		}

		productGridElement.append(...cards);
	}

	function makeCard(item) {
		const baseUrl = window.location.origin;

		// Create elements
		const cardElement = document.createElement('div');
		cardElement.classList.add('product-item');

		const productFilterElement = document.createElement('div');
		productFilterElement.classList.add('product', 'product_filter');
		if (item['is_discounted']) {
			productFilterElement.classList.add('discount');
		}

		const wrapperAElement = document.createElement('a');
		wrapperAElement.classList.add('product_image');
		wrapperAElement.href = `/items/${item.slug}/`;

		const imgElement = document.createElement('img');
		imgElement.loading = 'lazy';
		const picture = item.pictures[0];
		if (picture) {
			imgElement.src = picture['image_url'];
			imgElement.alt = 'продуктово изображение';
		} else {
			imgElement.src = `${baseUrl}static/images/item.jpg`;
			imgElement.alt = 'no image';
		}

		const heartElement = document.createElement('div');
		if (item['is_discounted']) {
			heartElement.classList.add('favorite', 'favorite_left');
		} else {
			heartElement.classList.add('favorite');
		}
		
		const tagElement = document.createElement('div');
		const innerTagElement = document.createElement('span');
		if (item['is_discounted']) {
			tagElement.classList.add('product_bubble', 'product_bubble_right', 'product_bubble_red', 'd-flex', 'flex-column', 'align-items-center');
			innerTagElement.textContent = `-${Number.parseInt(item.discount)}€`;
		} else if (item['is_new']) {
			tagElement.classList.add('product_bubble', 'product_bubble_left', 'product_bubble_green', 'd-flex', 'flex-column', 'align-items-center');
			innerTagElement.textContent = translations.new;
		}

		const productInfoElement = document.createElement('div');
		productInfoElement.classList.add('product_info');

		const productNameElement = document.createElement('p');
		productNameElement.classList.add('product_name');

		const nameAElement = document.createElement('a');
		nameAElement.href = `${baseUrl}items/${item.slug}`;
		nameAElement.textContent = item.name;

		const priceElement = document.createElement('div');
		priceElement.classList.add('product_price');
		if (item['is_discounted']) {
			priceElement.textContent = `${item['discount_price']} €`;
		} else {
			priceElement.textContent = `${item.price} €`;
		}

		const secondaryPriceElement = document.createElement('span');
		secondaryPriceElement.classList.add('price_eur');
		if (item['is_discounted']) {
			secondaryPriceElement.textContent = `/${item['discount_price_bgn']} ${translations.lv}`;
		} else {
			secondaryPriceElement.textContent = `/${item['price_bgn']} ${translations.lv}`;
		}

		const buyDivElement = document.createElement('div');
		buyDivElement.classList.add('red_button', 'add_to_cart_button');

		const buyAElement = document.createElement('a');
		buyAElement.href = `/items/${item.slug}`;
		buyAElement.textContent = translations.get;

		// Assemble card
		cardElement.append(productFilterElement);
		productFilterElement.append(wrapperAElement);
		wrapperAElement.append(imgElement);
		productFilterElement.append(heartElement);

		if (item['is_discounted'] || item['is_new']) {
			productFilterElement.append(tagElement);
			tagElement.append(innerTagElement);
		}
		
		productFilterElement.append(productInfoElement);
		productInfoElement.append(productNameElement);
		productNameElement.append(nameAElement);
		productInfoElement.append(priceElement);
		priceElement.append(secondaryPriceElement);
		cardElement.append(buyDivElement);
		buyDivElement.append(buyAElement);

		return cardElement;
	}
});