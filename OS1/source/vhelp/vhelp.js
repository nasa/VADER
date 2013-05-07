/* Help overlay. Requires jquery.
*/

var $_vhelp = null; // The outer div
var $_vhelp_ary; // The active screen elements
var $_vhelp_btn_exit; // Closes the help

	// Flag when true means the associated subup (sub-popup) is showing
var vhelp_is_showing_out = false;
var vhelp_is_showing_in  = false;
var vhelp_is_showing_sgl = false;
var vhelp_is_showing_mlt = false;
var vhelp_is_showing_pwr = false;
var vhelp_is_showing_dflt = false;
var vhelp_is_showing_chn = false;
	// When true any subup is showing
function vhelp_is_showing_subpup() { return (vhelp_is_showing_out || vhelp_is_showing_in || vhelp_is_showing_sgl || vhelp_is_showing_mlt || vhelp_is_showing_pwr || vhelp_is_showing_dflt || vhelp_is_showing_chn); }

var $_vhelp_subup; // The outer div for a subup, common among all subups
var $_vhelp_subup_title; // The element containing the title for each subup
var $_vhelp_subup_info; // The element containing the content for each subup


	// Dynamic mouse effects...
function vhelp_effect_set( $o, new_class )
{
	if( $o )
	{
		$o.removeClass( "vhelp-effect-none vhelp-effect-click vhelp-effect-hover" );
		if( new_class )
			$o.addClass( new_class );
	}
}

function vhelp_menter( $o )
{
	vdest_css_cursor_pointer( $o );
	vhelp_effect_set( $o.find(".vhelp-info-item"), "vhelp-effect-hover" ); // Cant get the effect to work on the $o div, so apply it only to the text
}
function vhelp_mleave( $o )
{
	vdest_css_cursor_default( $o );
	vhelp_effect_set( $o.find(".vhelp-info-item"), null );
}
function vhelp_mdown( $o )
{
	vhelp_effect_set( $o.find(".vhelp-info-item"), "vhelp-effect-click" );
	$o.css( "opacity", 0.3 );
}
function vhelp_mup( $o )
{
	vhelp_effect_set( $o.find(".vhelp-info-item"), "vhelp-effect-hover" );
	$o.css( "opacity", 1.0 );
}

	// Generates the html for the help outer div and the subup div
function vhelp_create( fn_exit )
{
	$(document.body).append( '\
		<div id="vhelp-cntnr-mn" class="vhelp-cntnr vhelp-bkg">\
			<img id="vhelp-btn-x"  src="vhelp/img/vhelp-btn-x.png">\
			<div class="vhelp-title vhelp-bkg"><i><span style="font-size:larger;">A</span>bout&nbsp;the&nbsp;<span style="font-size:larger;">D</span>isplay&nbsp;<span style="font-size:larger;">C</span>ontrol...</i></div>\
			<div class="vhelp-info-cntnr">\
				<img class="info-icon newln" src="vhelp/img/vhelp-info-lg.png">\
				<div class="vhelp-info-intro">\
					This tool provides a user the ability to control the inputs being displayed on the outputs in the Ops&nbsp;Suite&nbsp;1.<br/>\
					Click on any of the following for more information\
				</div>\
				<div id="h-cap-about-out" class="newln indent">\
					<img src="vhelp/img/vhelp-bullet.png">\
					<span class="vhelp-info-item vhelp-cap-bkg">About Outputs</span>\
				</div>\
				<div id="h-cap-about-in" class="newln indent">\
					<img src="vhelp/img/vhelp-bullet.png">\
					<span class="vhelp-info-item vhelp-cap-bkg">About Inputs </span>\
				</div>\
				<div id="h-cap-input-single" class="newln indent">\
					<img src="vhelp/img/vhelp-bullet.png">\
					<span class="vhelp-info-item vhelp-cap-bkg">Change the Input Source for a single display</span>\
				</div>\
				<div id="h-cap-input-multi" class="newln indent">\
					<img src="vhelp/img/vhelp-bullet.png">\
					<span class="vhelp-info-item vhelp-cap-bkg">Change the Input Source for multiple displays at once</span>\
				</div>\
				<div id="h-cap-power" class="newln indent">\
					<img src="vhelp/img/vhelp-bullet.png">\
					<span class="vhelp-info-item vhelp-cap-bkg">Turn a display on or off</span>\
				</div>\
				<div id="h-cap-default" class="newln indent">\
					<img src="vhelp/img/vhelp-bullet.png">\
					<span class="vhelp-info-item vhelp-cap-bkg">Reset to the default configuration</span>\
				</div>\
				<div id="h-cap-tvchan" class="newln indent">\
					<img src="vhelp/img/vhelp-bullet.png">\
					<span class="vhelp-info-item vhelp-cap-bkg">Change the cable-TV channel </span>\
				</div>\
			</div>\
			<!--div class="disclaimer">These pages are best viewed on anything but Internet Explorer.</div-->\
		</div>\
		<div id="vhelp-cntnr-subup" class="vhelp-cntnr vhelp-bkg">\
			<img id="vhelp-subup-x"  src="vhelp/img/vhelp-btn-x.png">\
			<div class="vhelp-title vhelp-bkg"></div>\
			<div class="vhelp-info-cntnr">\
				<img class="info-icon newln" src="vhelp/img/vhelp-info.png">\
				<div class="vhelp-info-intro">\
				</div>\
				<div id="vhelp-subup-back" class="newln indent">\
					<img class="back-icon" src="vhelp/img/vhelp-back.png">\
					<span class="vhelp-goback"><i>Go Back</i></span>\
				</div>\
			</div>\
		</div>'	);

	$_vhelp = $( "#vhelp-cntnr-mn" );

	$_vhelp_ary = new Array ( $( "#h-cap-about-out" ), $( "#h-cap-about-in" ), $( "#h-cap-input-single" ), $( "#h-cap-input-multi" ), $( "#h-cap-power" ), $( "#h-cap-default" ), $( "#h-cap-tvchan" ) );

		// Mouse down/up the same for all main help active screen elements
	for( var bx = 0; bx < $_vhelp_ary.length; bx++ )
	{
		$_vhelp_ary[bx]
		.mousedown( function() { vhelp_mdown( $(this) ); return false; } )
		.mouseup(   function() { vhelp_mup( $(this) ); return false; } );
	}//for bx

		// Each main help page active screen element has unique click, mouseenter, mouseleave functionality
	$_vhelp_ary[0].click( function()              // ABOUT OUTPUTS
	{
			// Creates the "about outputs" subup, passes in an exit function that gets called when the subub is closed
			// 'xit' when true means the X button was clicked - exit all the way out of help
			// 'xit' when false means to exit the subup, then show the main help page
		vhelp_subup_create_out( function( xit )//exit 'out'
		{
			vhelp_is_showing_out = false;

				// Clear the hilights on the home page
			for( var dx = 0; dx < $_vdestinations.length; dx++ )
				$_vdestinations[dx].removeClass( "vhelp-vdest-effect-bigger" );

			if( xit ) fn_exit(); // all the way out
			else _vhelp_show(); // show main help
		} );

			// Clear the mouse effects on the main help page active screen elements before showing the subup
		for( var bx = 0; bx < $_vhelp_ary.length; bx++ )
			vhelp_mleave( $_vhelp_ary[bx] );

		vhelp_is_showing_out = true;
		_vhelp_hide(); // Hide the main help page
		vhelp_subup_show(); // Show the subup

			// Hilight the outputs on the home (vdest) page when this subup is shown
		for( var dx = 0; dx < $_vdestinations.length; dx++ )
			$_vdestinations[dx].addClass( "vhelp-vdest-effect-bigger" );
		return false;
	} )
	.mouseenter( function() { vhelp_menter( $(this) ); return false; } )
	.mouseleave( function() { vhelp_mleave( $(this) ); return false; } );

	$_vhelp_ary[1].click( function()              // ABOUT INPUTS
	{
		vhelp_subup_create_in( function( xit )//exit 'in'
		{
			vhelp_is_showing_in = false;
			if( xit ) fn_exit();
			else _vhelp_show();
		} );
		
		for( var bx = 0; bx < $_vhelp_ary.length; bx++ )
			vhelp_mleave( $_vhelp_ary[bx] );
		
		vhelp_is_showing_in = true;
		_vhelp_hide();
		vhelp_subup_show();
		return false;
	} )
	.mouseenter( function() { vhelp_menter( $(this) ); return false; } )
	.mouseleave( function() { vhelp_mleave( $(this) ); return false; } );

	$_vhelp_ary[2].click( function()              // OUTPUT SINGLE SELECT
	{
		vhelp_subup_create_sgl( function( xit )//exit sgl
		{
			vhelp_is_showing_sgl = false;
			if( xit ) fn_exit();
			else _vhelp_show();
			$_vdestinations[3].removeClass( "vhelp-vdest-effect-bigger" );
		} );
		
		for( var bx = 0; bx < $_vhelp_ary.length; bx++ )
			vhelp_mleave( $_vhelp_ary[bx] );
		
		vhelp_is_showing_sgl = true;
		_vhelp_hide();
		vhelp_subup_show();

			// Remove the vdest main page mouseover hilights
		for( var dx = 0; dx < $_vdestinations.length; dx++ )
			$_vdestinations[dx].removeClass( "vhelp-vdest-effect-bigger" );

			// When the sgl subup is shown, hilight the example output device for this subup to reference
		$_vdestinations[3].addClass( "vhelp-vdest-effect-bigger" );

		return false;
	} ).mouseenter( function()
	{
		if( !vhelp_is_showing_sgl )
		{
			vhelp_menter( $(this) );
				// Hilight all the output devices on the vdest main page
			for( var dx = 0; dx < $_vdestinations.length; dx++ )
				$_vdestinations[dx].addClass( "vhelp-vdest-effect-bigger" );
		}
		return false;
	} ).mouseleave( function()
	{
			// Perform the mouse effect only when the subup is NOT being shown.
			// Performing a mouseleave when the subup is shown will clear the hilighted output that the subup references
		if( !vhelp_is_showing_sgl )
		{
			vhelp_mleave( $(this) );

				// Remove hilights from the output devices on the vdest main page
			for( var dx = 0; dx < $_vdestinations.length; dx++ )
				$_vdestinations[dx].removeClass( "vhelp-vdest-effect-bigger" );
		}
		return false;
	} );

	$_vhelp_ary[3].click( function()              // CHECKBOX MULTI SELECT
	{
		vhelp_subup_create_mlt( function( xit )//exit mlt
		{
			vhelp_is_showing_mlt = false;
			if( xit ) fn_exit();
			else _vhelp_show();
			vdest_cbox_uncheck( $_vdestinations[0], null );
			vdest_cbox_uncheck( $_vdestinations[2], null );
			vdest_cbox_uncheck( $_vdestinations[4], null );
			$_vdest_btn_selected.removeClass( "vhelp-vdest-effect-bigger" );
			vdest_btn_selected_hide();
		} );
		for( var bx = 0; bx < $_vhelp_ary.length; bx++ )
			vhelp_mleave( $_vhelp_ary[bx] );
		vhelp_is_showing_mlt = true;
		_vhelp_hide();
		vhelp_subup_show();

			// Clear all the checked boxes on the vdest main page
		for( var dx = 0; dx < $_vdestinations.length; dx++ )
			$_vdestinations[dx].find( ".vdest-tvbtn-cbox" ).attr( "src", "img/cbox_clr.png" );

			// Check a few example boxes for the subup to reference
		vdest_cbox_check( $_vdestinations[0], null );
		vdest_cbox_check( $_vdestinations[2], null );
		vdest_cbox_check( $_vdestinations[4], null );
		vdest_btn_selected_show();

			// Hilight the active element on the vdest main page. The mlt subup points to it.
		$_vdest_btn_selected.addClass( "vhelp-vdest-effect-bigger" );
		return false;
	} ).mouseenter( function()
	{
		if( !vhelp_is_showing_mlt )
		{
			vhelp_menter( $(this) );
			for( var dx = 0; dx < $_vdestinations.length; dx++ )
				$_vdestinations[dx].find( ".vdest-tvbtn-cbox" ).attr( "src", "img/cbox_chk.png" );
		}
		return false;
	} ).mouseleave( function()
	{
		if( !vhelp_is_showing_mlt )
		{
			vhelp_mleave( $(this) );
			for( var dx = 0; dx < $_vdestinations.length; dx++ )
				$_vdestinations[dx].find( ".vdest-tvbtn-cbox" ).attr( "src", "img/cbox_clr.png" );
		}
		return false;
	} );

	$_vhelp_ary[4].click( function()              // POWER TOGGLE
	{
		vhelp_subup_create_pwr( function( xit )//exit pwr
		{
			vhelp_is_showing_pwr = false;
			if( xit ) fn_exit();
			else _vhelp_show();
			$_vdestinations[5].find( ".vdest-tvbtn-power" ).removeClass( "vhelp-vdest-effect-bigger" );
		} );
		for( var bx = 0; bx < $_vhelp_ary.length; bx++ )
			vhelp_mleave( $_vhelp_ary[bx] );
		vhelp_is_showing_pwr = true;
		_vhelp_hide();
		vhelp_subup_show();

			// Hilight all the power buttons on the outputs on the vdest main page
		for( var dx = 0; dx < $_vdestinations.length-2; dx++ )
			$_vdestinations[dx].find( ".vdest-tvbtn-power" ).removeClass( "vhelp-vdest-effect-bigger" );

			// Hilight a sample power button on the vdest main page. This subup points to it
		$_vdestinations[5].find( ".vdest-tvbtn-power" ).addClass( "vhelp-vdest-effect-bigger" );
		return false;
	} ).mouseenter( function()
	{
		if( !vhelp_is_showing_pwr )
		{
			vhelp_menter( $(this) );
			for( var dx = 0; dx < $_vdestinations.length-2; dx++ )
				$_vdestinations[dx].find( ".vdest-tvbtn-power" ).addClass( "vhelp-vdest-effect-bigger" );
		}
		return false;
	} ).mouseleave( function()
	{
		if( !vhelp_is_showing_pwr )
		{
			vhelp_mleave( $(this) );
			for( var dx = 0; dx < $_vdestinations.length-2; dx++ )
				$_vdestinations[dx].find( ".vdest-tvbtn-power" ).removeClass( "vhelp-vdest-effect-bigger" );
		}
		return false;
	} );

	$_vhelp_ary[5].click( function()              // DEFAULT SETUP
	{
		vhelp_subup_create_dflt( function( xit )//exit dflt
		{
			vhelp_is_showing_dflt = false;
			if( xit ) fn_exit();
			else _vhelp_show();
			$( ".vdest-btn-default" ).removeClass( "vhelp-vdest-effect-bigger" );
		} );
		for( var bx = 0; bx < $_vhelp_ary.length; bx++ )
			vhelp_mleave( $_vhelp_ary[bx] );
		vhelp_is_showing_dflt = true;
		_vhelp_hide();
		vhelp_subup_show();

			// Hilight the "Default Config" active element on the vdest main page. This subup points to it
		$( ".vdest-btn-default" ).addClass( "vhelp-vdest-effect-bigger" );
		return false;
	} ).mouseenter( function()
	{
		if( !vhelp_is_showing_dflt )
		{
			vhelp_menter( $(this) );
			$( ".vdest-btn-default" ).addClass( "vhelp-vdest-effect-bigger" );
		}
		return false;
	} ).mouseleave( function()
	{
		if( !vhelp_is_showing_dflt )
		{
			vhelp_mleave( $(this) );
			$( ".vdest-btn-default" ).removeClass( "vhelp-vdest-effect-bigger" );
		}
		return false;
	} );

	$_vhelp_ary[6].click( function()              // CHANGE CHANNEL
	{
		vhelp_subup_create_chn( function( xit )//exit chn
		{
			vhelp_is_showing_chn = false;
			if( xit ) fn_exit();
			else _vhelp_show();
			$( ".vdest-btn-numpad" ).removeClass( "vhelp-vdest-effect-bigger" );
		} );
		for( var bx = 0; bx < $_vhelp_ary.length; bx++ )
			vhelp_mleave( $_vhelp_ary[bx] );
		vhelp_is_showing_chn = true;
		_vhelp_hide();
		vhelp_subup_show();

			// Hilight the "Change Channel" active element on the vdest main page. This subup points to it
		$( ".vdest-btn-numpad" ).addClass( "vhelp-vdest-effect-bigger" );
		return false;
	} ).mouseenter( function()
	{
		if( !vhelp_is_showing_chn )
		{
			vhelp_menter( $(this) );
			$( ".vdest-btn-numpad" ).addClass( "vhelp-vdest-effect-bigger" );
		}
		return false;
	} ).mouseleave( function()
	{
		if( !vhelp_is_showing_chn )
		{
			vhelp_mleave( $(this) );
			$( ".vdest-btn-numpad" ).removeClass( "vhelp-vdest-effect-bigger" );
		}
		return false;
	} );

	$_vhelp_btn_exit = $( "#vhelp-btn-x" ).click( function()               //////// EXIT -- Close the help
	{
			// Clear any residual effects
		for( var dx = 0; dx < $_vdestinations.length; dx++ )
		{
			$_vdestinations[dx].removeClass( "vhelp-vdest-effect-bigger" );
			$_vdestinations[dx].find( ".vdest-tvbtn-cbox" ).attr( "src", "img/cbox_clr.png" );
			$_vdestinations[dx].find( ".vdest-tvbtn-power" ).removeClass( "vhelp-vdest-effect-bigger" );
		}
		$( ".vdest-btn-default" ).removeClass( "vhelp-vdest-effect-bigger" );
		$( ".vdest-btn-numpad" ).removeClass( "vhelp-vdest-effect-bigger" );

		_vhelp_hide();
		fn_exit();
		return false;
	} )
	.mouseenter( function() { $(this).css( "cursor", "pointer" ); return false; } )
	.mouseleave( function() { vdest_css_cursor_default( $(this) ); return false; } )
	.mousedown(  function() { vhelp_mdown( $(this) ); return false; } )
	.mouseup(    function() { vhelp_mup( $(this) ); vhelp_effect_set( $(this), null ); return false; } );



																							/********************/
																							/********************/
																							/*******************    S U B U P ' s   ***/
																							/********************/
																							/********************/


	$_vhelp_subup = $( "#vhelp-cntnr-subup" );
	$_vhelp_subup_title = $_vhelp_subup.find( ".vhelp-title" );
	$_vhelp_subup_info = $_vhelp_subup.find( ".vhelp-info-intro" );

	$( "#vhelp-subup-x" )
	.click(    function() { vhelp_subup_hide(); vhelp_subup_fn_exit(true); return false; } )
	.mouseenter( function() { $(this).css( "cursor", "pointer" ); return false; } )
	.mouseleave( function() { vdest_css_cursor_default( $(this) ); return false; } )
	.mousedown(  function() { vhelp_mdown( $(this) ); return false; } )
	.mouseup(    function() { vhelp_mup( $(this) ); vhelp_effect_set( $(this), null ); return false; } );
	$( "#vhelp-subup-back" )
	.click( function() { vhelp_subup_hide(); vhelp_subup_fn_exit(false); return false; } )
	.mouseenter( function() { vdest_css_cursor_pointer( $(this) ); vhelp_effect_set( $(this).find(".vhelp-goback"), "vhelp-effect-hover" ); return false; } )
	.mouseleave( function() { vdest_css_cursor_default( $(this) ); vhelp_effect_set( $(this).find(".vhelp-goback"), null ); return false; } )
	.mousedown(  function() { vhelp_mdown( $(this) ); return false; } )
	.mouseup(    function() { vhelp_mup( $(this) ); vhelp_effect_set( $(this), null ); return false; } );

}// _create()

	// Emulate a mouse click
function vhelp_mouseclick_emul( $o )
{
	$o.mousedown().click();
	setTimeout( function()
	{
		$o.mouseup();
		vhelp_effect_set( $o, null );
	}, 40 );
}

	// Capture the escape key to exit
function vhelp_keyup( evt )
{
	if( evt.keyCode === 27/*escape*/ )
	{
		if( $_vhelp.is(":visible") )
			vhelp_mouseclick_emul( $_vhelp_btn_exit );
		else if( vhelp_is_showing_subpup() )
			vhelp_mouseclick_emul( $("#vhelp-subup-x") );
	}
}


	// Size, position, and scale a subup
function $_vhelp_subup_size_and_offset_set( $o, height, proportions, offset, font_size, font_size_title )
{
	if( $o )
	{
		$o.height( height );
		$o.width( height * proportions ); // ratio of the dimensions of the bkg img
		$o.css( "font-size", font_size );
		$o.find( ".vhelp-title" ).css( "font-size", font_size_title );
		$o.css( { top:offset.top, left:offset.left } );
	}
}

	// Location data for each subup
var hlp_posn      = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };
var hlp_posn_out  = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };
var hlp_posn_in   = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };
var hlp_posn_sgl  = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };
var hlp_posn_mlt  = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };
var hlp_posn_pwr  = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };
var hlp_posn_dflt = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };
var hlp_posn_chn  = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };

	// Sizing data
var hlp_size_out  = { height:100, props:1.4 };
var hlp_size_in   = { height:100, props:1.4 };
var hlp_size_sgl  = { height:100, props:1.4 };
var hlp_size_mlt  = { height:100, props:1.4 };
var hlp_size_pwr  = { height:100, props:1.4 };
var hlp_size_dflt = { height:100, props:1.4 };
var hlp_size_chn  = { height:100, props:1.4 };

var font_size;
var font_size_title;


function vhelp_size_and_offset_set( height, l_top, l_left )
{
		// Html fonts don't scale when the screen resizes, so do it in script
	font_size = height * 0.0500;
	font_size_title = height * 0.066;
	var hlp_props_default = 876 / 512; // Dimensions of the background image
	$( "#vhelp-subup-x" ).width( height * 0.099 ).height( height * 0.099 ); // Scale the exit button

		// The main help dialog
	hlp_posn.show = { top:l_top, left:l_left };
	$_vhelp_subup_size_and_offset_set( $_vhelp, height, hlp_props_default, hlp_posn.show, font_size, font_size_title );

	var hlp_width_max = $_vhelp.width();

		// Recalculate the subup's too
	hlp_posn_out.show  = hlp_posn_out.hide = { top:l_top + (height * 0.20), left:l_left + (hlp_width_max * 0.44) };
	hlp_size_out.height = height * 0.63;
	hlp_size_out.props = hlp_props_default * 0.9;

	hlp_posn_in.show   = hlp_posn_in.hide = { top:l_top + (height * 0.10), left:l_left + (hlp_width_max * 0.10) };
	hlp_size_in.height = height * 0.70;
	hlp_size_in.props = hlp_props_default;

	hlp_posn_sgl.show  = hlp_posn_sgl.hide = { top:l_top + (height * 0.25), left:l_left - (hlp_width_max * 0.10) };
	hlp_size_sgl.height = height * 0.75;
	hlp_size_sgl.props = hlp_props_default;

	hlp_posn_mlt.show  = hlp_posn_mlt.hide = { top:l_top + (height * 0.070), left:l_left - (hlp_width_max * 0.27) };
	hlp_size_mlt.height = height * 0.85;
	hlp_size_mlt.props = hlp_props_default;

	hlp_posn_pwr.show  = hlp_posn_pwr.hide = { top:l_top + (height * 0.32), left:l_left + (hlp_width_max * 0.07) };
	hlp_size_pwr.height = height * 0.45;
	hlp_size_pwr.props = hlp_props_default;

	hlp_posn_dflt.show = hlp_posn_dflt.hide = { top:l_top + (height * 0.07), left:l_left - (hlp_width_max * 0.02) };
	hlp_size_dflt.height = height * 0.52
	hlp_size_dflt.props = hlp_props_default;

	hlp_posn_chn.show  = hlp_posn_chn.hide = { top:l_top + (height * 0.14), left:l_left - (hlp_width_max * 0.02) };
	hlp_size_chn.height = height * 0.52;
	hlp_size_chn.props = hlp_props_default;

	vhelp_subup_size_and_offset_set();
}

function _vhelp_show() // internally accessed
{
	os1_popup_show( $_vhelp, 400, hlp_posn.hide, hlp_posn.show );
}

function vhelp_show( offset ) // external - called from vdest main page
{
	hlp_posn.hide = offset;
	os1_popup_show( $_vhelp, 400, hlp_posn.hide, hlp_posn.show );
}

function _vhelp_hide() // internal
{
	os1_popup_hide( $_vhelp, 400, hlp_posn.hide );
}


										/**************************** SUB-POPUPs
                                         ****************************/

var vhelp_subup_fn_exit; // The function to call when a subup is closed
var vhelp_subup_posn; // Global position of the currently shown subup, set when the subup is shown
var vhelp_subup_size; // Global size of the currently shown subup, set when it is shown

function vhelp_subup_size_and_offset_set()
{
	if( vhelp_is_showing_out )
	{
		vhelp_subup_posn = hlp_posn_out;
		vhelp_subup_size = hlp_size_out;
	} else if( vhelp_is_showing_in )
	{
		vhelp_subup_posn = hlp_posn_in;
		vhelp_subup_size = hlp_size_in;
	} else if( vhelp_is_showing_sgl )
	{
		vhelp_subup_posn = hlp_posn_sgl;
		vhelp_subup_size = hlp_size_sgl;
	} else if( vhelp_is_showing_mlt )
	{
		vhelp_subup_posn = hlp_posn_mlt;
		vhelp_subup_size = hlp_size_mlt;
	} else if( vhelp_is_showing_pwr )
	{
		vhelp_subup_posn = hlp_posn_pwr;
		vhelp_subup_size = hlp_size_pwr;
	} else if( vhelp_is_showing_dflt )
	{
		vhelp_subup_posn = hlp_posn_dflt;
		vhelp_subup_size = hlp_size_dflt;
	} else if( vhelp_is_showing_chn )
	{
		vhelp_subup_posn = hlp_posn_chn;
		vhelp_subup_size = hlp_size_chn;
	}

	if( vhelp_is_showing_subpup() )
	{
		$_vhelp_subup_size_and_offset_set( $_vhelp_subup, vhelp_subup_size.height, vhelp_subup_size.props, vhelp_subup_posn.show, font_size * 0.95, font_size_title * 0.95 ); // Scale down the fonts a bit in the subups
	}
}


function vhelp_subup_hide()
{
	os1_popup_hide( $_vhelp_subup, 400, vhelp_subup_posn.hide );
}

function vhelp_subup_show()
{
	vhelp_subup_size_and_offset_set();
	os1_popup_show( $_vhelp_subup, 400, vhelp_subup_posn.hide, vhelp_subup_posn.show );
}


										/**************************** ABOUT OUTPUTS POPUP */

function vhelp_subup_create_out( fn_exit )
{
	vhelp_subup_fn_exit = fn_exit;
	$_vhelp_subup_title.html( '<i><span style="font-size:larger;">A</span>bout&nbsp;<span style="font-size:larger;">O</span>utputs</i>' );
	$_vhelp_subup_info.html(
		'Highlighted here are the six Displays in Ops Suite&nbsp;1. Also highlighted are the two Outputs that will direct an input source back to the Main MCC video switch.' );
}

										/**************************** ABOUT INPUTS POPUP */

function vhelp_subup_create_in( fn_exit )
{
	vhelp_subup_fn_exit = fn_exit;
	$_vhelp_subup_title.html( '<i><span style="font-size:larger;">A</span>bout&nbsp;<span style="font-size:larger;">I</span>nputs</i>' );
	$_vhelp_subup_info.html(
		'Once an Output has been selected, the Input Source Panel <img class="vsrc-icon" src="vhelp/img/vsrc.jpg"> will pop up listing the eight Inputs from which the user \
		can select to display on the selected Output.' );
}

										/**************************** SINGLE SELECTED POPUP */

function vhelp_subup_create_sgl( fn_exit )
{
	vhelp_subup_fn_exit = fn_exit;
	$_vhelp_subup_title.html( '<i><span style="font-size:larger;">S</span>ingle&nbsp;<span style="font-size:larger;">O</span>utput&nbsp;<span style="font-size:larger;">S</span>election </i>' );
	$_vhelp_subup_info.html(
		'When a single Output has been selected, the Input Source Panel <img class="vsrc-icon" src="vhelp/img/vsrc.jpg"> is used to connect \
		an Input source to the Output. Power and volume for the Output can be controlled using the buttons on the right.' );
}

										/**************************** MULTIPLE SELECTED POPUP */

function vhelp_subup_create_mlt( fn_exit )
{
	vhelp_subup_fn_exit = fn_exit;
	$_vhelp_subup_title.html( '<i><span style="font-size:larger;">M</span>ultiple&nbsp;<span style="font-size:larger;">O</span>utput&nbsp;<span style="font-size:larger;">S</span>election </i>' );
	$_vhelp_subup_info.html(
		'<img class="vhelp-arrow" src="vhelp/img/vhelp-arrow-20.png">\
		Clicking on the checkbox in the upper right-hand corner of the Output device allows the user to control more than one Output. \
		Click on "Process Selected Devices" to get the Input Source Panel so that an Input source can be connected <img class="vsrc-icon-mlt" src="vhelp/img/vsrc-mlt.jpg"> \
		to each Output device. The power and volume buttons will perform their respective functions on \
		each Output device.' );
}

										/**************************** POWER TOGGLE */

function vhelp_subup_create_pwr( fn_exit )
{
	vhelp_subup_fn_exit = fn_exit;
	$_vhelp_subup_title.html( '<i><span style="font-size:larger;">P</span>ower&nbsp;<span style="font-size:larger;">D</span>isplay</i>' );
	$_vhelp_subup_info.html(
		'Click on the power button in the lower right-hand corner of the Display to turn it on or off.\
		<img class="vhelp-arrow-pwr newln" src="vhelp/img/vhelp-ltarrow.png">' );
}

										/**************************** DEFAULT CONFIG */

function vhelp_subup_create_dflt( fn_exit )
{
	vhelp_subup_fn_exit = fn_exit;
	$_vhelp_subup_title.html( '<i><span style="font-size:larger;">R</span>eset&nbsp;<span style="font-size:larger;">C</span>onfiguration</i>' );
	$_vhelp_subup_info.html(
		'Click on the "Default Configuration" button to reset all the Displays to their default Inputs.\
		<img class="vhelp-arrow-dflt newln" src="vhelp/img/vhelp-rtarrow.png">' );
}

										/**************************** CHANNEL */

function vhelp_subup_create_chn( fn_exit )
{
	vhelp_subup_fn_exit = fn_exit;
	$_vhelp_subup_title.html( '<i><span style="font-size:larger;">C</span>hange&nbsp;<span style="font-size:larger;">C</span>hannel</i>' );
	$_vhelp_subup_info.html(
		'Click on the "Change TV Channel" button to change the channel on the Cable TV Input source.\
		<img class="vhelp-arrow-chn newln" src="vhelp/img/vhelp-rtarrow.png">' );
}
