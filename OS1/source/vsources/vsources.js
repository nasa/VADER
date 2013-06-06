/* Video input source selection popup. Requires jquery.
*/

var $_vsources_cntnr;
var $_vsources;
var $_sbtn_exit;
var $_sbtn_power;
var $_sbtn_volup;
var $_sbtn_voldn;
var $_sbtn_mute;
var $_vsrc_headr;


var fn_status_msg;

function vsrc_status_set( msg )
{
	if( fn_status_msg )fn_status_msg( msg || "Click on an input source to show on the selected output device(s)." );
}


function vsources_$( jx   ) { return $_vsources[jx]; }
function vsources_$_tv()    { return $_vsources[4]; }
function vsources_$_hevs1() { return $_vsources[5]; }
function vsources_$_hevs2() { return $_vsources[6]; }
function vsources_$_hevs3() { return $_vsources[7]; }


function vsrc_effect_set( $o, new_class )
{
	if( $o )
	{
		$o.removeClass( "vsrc-effect-none vsrc-effect-click vsrc-effect-hover vsrc-effect-hover-btn vsrc-effect-connected" );
		if( new_class )
			$o.addClass( new_class );
	}
}

function vsrc_mouseenter( $o, statmsg )
{
	vdest_css_cursor_pointer( $o );
	vsrc_effect_set( $o, "vsrc-effect-hover-btn" );
	vsrc_status_set( statmsg );
}
function vsrc_mouseleave( $o )
{
	vdest_css_cursor_default( $o );
	vsrc_effect_set( $o, null );
	vsrc_status_set( null );
}
function vsrc_mousedown( $o )
{
	vsrc_effect_set( $o, "vsrc-effect-click" );
	$o.css( "opacity", 0.3 );
}
function vsrc_mouseup( $o )
{
	vsrc_effect_set( $o, "vsrc-effect-hover-btn" );
	$o.css( "opacity", 1.0 );
}


// Generate the html for vsources
function vsources_create( fn_status, fn_exit, fn_volume, fn_power, fn_vsrc_click, fn_$_connected_to )
{
	$(document.body).append('\
		<div id="vsource-cntnr" class="vsource-cntnr-brdr vsource-cntnr-bkg vsrc-bkg">\
			<div id="vsource-header">&nbsp;</div>\
			<img class="vsrc-btn-exit vsrc-btn vsrc-bkg"  src="vsources/img/src-btn-close.jpg">\
			<div class="vsource-cntnr-inputs">\
				<img id="vsrc-appletv"    class="vsource vsrc-bkg" data-input="5" data-name_of="AppleTV"      src="vsources/img/appletv.png">\
				<img id="vsrc-widi"       class="vsource vsrc-bkg" data-input="6" data-name_of="WiDi"         src="vsources/img/intel_widi.png">\
				<img id="vsrc-clickshare" class="vsource vsrc-bkg" data-input="1" data-name_of="ClickShare"   src="vsources/img/clickshare.png">\
				<img id="vsrc-vader"      class="vsource vsrc-bkg" data-input="7" data-name_of="VADER"        src="vsources/img/vader.png">\
				<img id="vsrc-hevs1"      class="vsource vsrc-bkg" data-input="2" data-name_of="MCC Video 1"  src="vsources/img/mcc_video1.png">\
				<img id="vsrc-hevs2"      class="vsource vsrc-bkg" data-input="3" data-name_of="MCC Video 2"  src="vsources/img/mcc_video2.png">\
				<img id="vsrc-hevs3"      class="vsource vsrc-bkg" data-input="4" data-name_of="MCC Video 3"  src="vsources/img/mcc_video3.png">\
				<img id="vsrc-tv"         class="vsource vsrc-bkg" data-input="8" data-name_of="Cable TV"     src="vsources/img/tv.png">\
			</div>\
			<div class="vsource-cntnr-btns">\
				<img class="vsrc-btn-power vsrc-btn vsrc-bkg"  src="vsources/img/src-btn-power.jpg">\
				<img class="vsrc-btn-mute  vsrc-btn vsrc-bkg"  src="vsources/img/src-btn-mute.jpg">\
				<img class="vsrc-btn-volup vsrc-btn vsrc-bkg"  src="vsources/img/src-btn-volup.jpg">\
				<img class="vsrc-btn-voldn vsrc-btn vsrc-bkg"  src="vsources/img/src-btn-voldn.jpg">\
			</div>\
		</div>');

	fn_status_msg = fn_status;

	$_vsources_cntnr = $( "#vsource-cntnr" ); // pop-up with input icons and buttons
	$_vsrc_headr = $( "#vsource-header" );

	$_vsources = new Array( $( "#vsrc-appletv" ), $( "#vsrc-widi" ), $( "#vsrc-clickshare" ), $( "#vsrc-vader" ), $( "#vsrc-tv" ), $( "#vsrc-hevs1" ), $( "#vsrc-hevs2" ), $( "#vsrc-hevs3" ) );

	for( var sx = 0; sx < $_vsources.length; sx++ )
	{
		vsrc_effect_set( $_vsources[sx], "vsrc-effect-none" );

		$_vsources[sx].data(
		{
			connected_to: null
		} ).click( function()							/************* INPUT SOURCE CLICK ************/
		{
			fn_vsrc_click ( $(this) );
			_vsources_hide();
			return false;
		} ).mouseenter( function()
		{
			vdest_css_cursor_pointer( $(this) );
			vsrc_effect_set( $(this), "vsrc-effect-hover" );
			vsrc_status_set( "Click to show the input source '" + $(this).data("name_of") + "'." );
			return false;
		} ).mouseleave( function()
		{
			var $o = $(this);
			vdest_css_cursor_default( $o );
			var iostate = "vsrc-effect-none";

				// If we mouseout of a source icon that has the 'connected_to' effect, reset that effect
			var $dest_connto = fn_$_connected_to();
			if( (null !== $dest_connto) && ($o[0] == $dest_connto[0]) )
				iostate = "vsrc-effect-connected";

			vsrc_effect_set( $o, iostate );
			vsrc_status_set( null );
			return false;
		} );
	}//for sx

	$_sbtn_exit = $_vsources_cntnr.find( ".vsrc-btn-exit" )						/************* SOURCE EXIT BUTTON ************/
		.click(      function() { _vsources_hide(); fn_exit(); return false; } )
		.mouseenter( function() { $(this).css( "cursor", "pointer" ); vsrc_status_set( "Exit input source selection." ); return false; } )
		.mouseleave( function() { vdest_css_cursor_default( $(this) ); vsrc_status_set( null ); return false; } )
		.mousedown(  function() { vsrc_mousedown( $(this) ); return false; } )
		.mouseup(    function() { vsrc_mouseup( $(this) ); vsrc_effect_set( $(this), null ); return false; } );

	$_sbtn_power = $_vsources_cntnr.find( ".vsrc-btn-power" )					/************* SOURCE POWER BUTTON ************/
		.click(      function() { fn_power(); return false; } )
		.mouseenter( function() { vsrc_mouseenter( $(this), "Click to cycle power on the selected output devices." ); return false; } )
		.mouseleave( function() { vsrc_mouseleave( $(this) ); return false; } )
		.mousedown(  function() { vsrc_mousedown( $(this) ); return false; } )
		.mouseup(    function() { vsrc_mouseup( $(this) ); return false; } );

	$_sbtn_volup = $_vsources_cntnr.find( ".vsrc-btn-volup" )					/************* SOURCE VOLUME UP BUTTON ************/
		.click(      function() { fn_volume( 1 ); return false; } )
		.mouseenter( function() { vsrc_mouseenter( $(this), "Click to increase volume on the selected output devices." ); return false; } )
		.mouseleave( function() { vsrc_mouseleave( $(this) ); return false; } )
		.mousedown(  function() { vsrc_mousedown( $(this) ); return false; } )
		.mouseup(    function() { vsrc_mouseup( $(this) ); return false; } );

	$_sbtn_voldn = $_vsources_cntnr.find( ".vsrc-btn-voldn" )					/************* SOURCE VOLUME DOWN BUTTON ************/
		.click(      function() { fn_volume( -1 ); return false; } )
		.mouseenter( function() { vsrc_mouseenter( $(this), "Click to decrease volume on the selected output devices." ); return false; } )
		.mouseleave( function() { vsrc_mouseleave( $(this) ); return false; } )
		.mousedown(  function() { vsrc_mousedown( $(this) ); return false; } )
		.mouseup(    function() { vsrc_mouseup( $(this) ); return false; } );

	$_sbtn_mute = $_vsources_cntnr.find( ".vsrc-btn-mute" )						/************* SOURCE MUTE BUTTON ************/
		.click(      function() { fn_volume( 0 ); return false; } )
		.mouseenter( function() { vsrc_mouseenter( $(this), "Click to cycle mute on the selected output devices." ); return false; } )
		.mouseleave( function() { vsrc_mouseleave( $(this) ); return false; } )
		.mousedown(  function() { vsrc_mousedown( $(this) ); return false; } )
		.mouseup(    function() { vsrc_mouseup( $(this) ); return false; } );

	if( os1_ie_uglify() )
	{
		$_vsources_cntnr.removeClass( "vsource-cntnr-bkg" ).addClass( "vsource-cntnr-bkg-ie" );
		$_vsources_cntnr.find( ".vsource-cntnr-inputs" ).addClass( "vsrc-cntnr-inputs-bkg-ie" );
		$_vsources_cntnr.find( ".vsource-cntnr-btns" ).addClass( "vsrc-cntnr-btns-bkg-ie" );
	}

}// _create()


function vsrc_mouseclick_emul( $o )
{
	$o.mousedown().click();
	setTimeout( function()
	{
		$o.mouseup();
		vsrc_effect_set( $o, null );
	}, 40 );
}

function vsources_keyup( evt )
{
	if( $_vsources_cntnr.is(":visible") )
	{
		switch( evt.keyCode )
		{
			case 27/*escape*/:  vsrc_mouseclick_emul( $_sbtn_exit ); break;// Close the source selection pop-up if the escape key was pressed
			case 107/*num+*/:
			case 61/*+*/:       vsrc_mouseclick_emul( $_sbtn_volup ); break;
			case 109/*num-*/:
			case 173/*-*/:	    vsrc_mouseclick_emul( $_sbtn_voldn ); break;
			case 49/*!*/:       /*vsrc_mouseclick_emul( $_sbtn_power );*/ break;
			case 50/*@*/:       /*vsrc_mouseclick_emul( $_sbtn_mute );*/ break;
			case 16/*Shft*/:     break;
			default:	//alert( "key: " + evt.keyCode );
		}
	}
}//_keyup()


var vsrc_hdr_fontsize = 10;
var vsrc_posn = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };

function vsrc_size_set( height ) { $_vsources_cntnr.height( height ).width( height * (781/489) ); } // dimensions of the image

function vsources_size_and_offset_set( height, l_top, l_left )
{
	vsrc_size_set( height );

		// Resize the source icons
	for( var sx = 0; sx < $_vsources.length; sx++ )
	{
		$_vsources[sx].height( height * 0.23 );
		$_vsources[sx].width( height * 0.23 );
	}

		// And the header font
	vsrc_hdr_fontsize = height * 0.052;
	$_vsrc_headr.css( "font-size", vsrc_hdr_fontsize );

	vsrc_posn.show = { top:l_top, left:l_left };
	$_vsources_cntnr.css( { top:l_top, left:l_left } ); // Use css to locate, .offset() doesn't work on hidden elements
}

function vsources_size_and_offset_set_center( height, height_cntnr )
{
	vsrc_size_set( height );
	vsources_size_and_offset_set( height, ((height_cntnr - $_vsources_cntnr.height()) / 2), (($("body" ).width() - $_vsources_cntnr.width()) / 2) );
}


function vsources_show( headermsg, a_hevs_is_selected, $vsrc_connected_to, offset )
{
	// Clear effects
	for( var sx = 0; sx < $_vsources.length; sx++ )
	{
		vsrc_effect_set( $_vsources[sx], "vsrc-effect-none" );
	}

	if( null !== $vsrc_connected_to )
		vsrc_effect_set( $vsrc_connected_to, "vsrc-effect-connected" );

	// if any HEVS destination is selected, remove the HEVS source's as an option
	for( sx = 4; sx < $_vsources.length; sx++ )
	{
		if( a_hevs_is_selected )
			$_vsources[sx].hide();
		else $_vsources[sx].show();
	}

	// If there are a bunch of outputs in the header, make the font for the text smaller
	if( headermsg.length > 56 )
		$_vsrc_headr.css( "font-size", vsrc_hdr_fontsize * 0.80 );
	else $_vsrc_headr.css( "font-size", vsrc_hdr_fontsize );

	$_vsrc_headr.html( "<span style='color:#cfc;'>Choose a Source for:</span> <b>" + headermsg + "</b>" );

	vsrc_posn.hide = offset;
	os1_popup_show( $_vsources_cntnr, 300, vsrc_posn.hide, vsrc_posn.show );
}

function _vsources_hide()
{
	os1_popup_hide( $_vsources_cntnr, 300, vsrc_posn.hide );
}

function vsource_for_inputnumber( inputn )
{
	for( var dx = 0; dx < $_vsources.length; dx++ )
	{
		if( inputn == $_vsources[dx].data( "input" ) )
			return $_vsources[dx];
	}
	return null;
}
