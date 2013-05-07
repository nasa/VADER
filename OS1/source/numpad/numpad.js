/* Number pad popup. Requires jquery.
*/

var $_btn_ary;
var $_btn_exit;
var $_numpad = null;
var $_channum = null;
var channum = "";
var text_is_volatile = true;
var close_on_enter = true;


function numpad_channelnumber_set( ch )
{
	channum = ch;
	$_channum.html( channum );
}


function npad_effect_set( $o, new_class )
{
	if( $o )
	{
		$o.removeClass( "numpad-effect-none numpad-effect-click numpad-effect-hover" );
		if( new_class )
			$o.addClass( new_class );
	}
}

function _mouseenter( $o )
{
	vdest_css_cursor_pointer( $o );
	npad_effect_set( $o, "numpad-effect-hover" );
}
function _mouseleave( $o )
{
	vdest_css_cursor_default( $o );
	npad_effect_set( $o, null );
}
function _mousedown( $o )
{
	npad_effect_set( $o, "numpad-effect-click" );
	$o.css( "opacity", 0.3 );
}
function _mouseup( $o )
{
	npad_effect_set( $o, "numpad-effect-hover" );
	$o.css( "opacity", 1.0 );
}


// Generate the html for numpad
function numpad_create( fn_exit, fn_channel )
{
		// The un-named div is an IE hack
	$(document.body).append('\
		<div id="numpad-cntnr" class="numpad-cntnr-brdr numpad-bkg">\
			<div>\
				<div id="npad-chn-win"   class="npad-chn-win-bkg npad-btn-brdr numpad-bkg"><span id="npad-channum-txt">0</span></div>\
				<img id="npad-btn-x"     class="npad-btn-brdr"        data-key="X"  src="numpad/img/npad-btn-x.jpg">\
			</div>\
			<img id="npad-btn-7"     class="npad-btn-brdr newln" data-key="7"  src="numpad/img/npad-btn-7.jpg">\
			<img id="npad-btn-8"     class="npad-btn-brdr"       data-key="8"  src="numpad/img/npad-btn-8.jpg">\
			<img id="npad-btn-9"     class="npad-btn-brdr"       data-key="9"  src="numpad/img/npad-btn-9.jpg">\
			<img id="npad-btn-4"     class="npad-btn-brdr newln" data-key="4"  src="numpad/img/npad-btn-4.jpg">\
			<img id="npad-btn-5"     class="npad-btn-brdr"       data-key="5"  src="numpad/img/npad-btn-5.jpg">\
			<img id="npad-btn-6"     class="npad-btn-brdr"       data-key="6"  src="numpad/img/npad-btn-6.jpg">\
			<img id="npad-btn-1"     class="npad-btn-brdr newln" data-key="1"  src="numpad/img/npad-btn-1.jpg">\
			<img id="npad-btn-2"     class="npad-btn-brdr"       data-key="2"  src="numpad/img/npad-btn-2.jpg">\
			<img id="npad-btn-3"     class="npad-btn-brdr"       data-key="3"  src="numpad/img/npad-btn-3.jpg">\
			<img id="npad-btn-dash"  class="npad-btn-brdr newln" data-key="."  src="numpad/img/npad-btn-dash.jpg">\
			<img id="npad-btn-0"     class="npad-btn-brdr"       data-key="0"  src="numpad/img/npad-btn-0.jpg">\
			<img id="npad-btn-enter" class="npad-btn-brdr"       data-key="13" src="numpad/img/npad-btn-enter.jpg">\
			<img id="npad-btn-chdn"  class="npad-btn-brdr newln" data-key="-"  src="numpad/img/npad-btn-chdn.jpg">\
			<img id="npad-btn-chup"  class="npad-btn-brdr"       data-key="+"  src="numpad/img/npad-btn-chup.jpg">\
			<img id="npad-btn-clear" class="npad-btn-brdr"       data-key="49" src="numpad/img/npad-btn-clear.jpg">\
		</div>');

	$_numpad = $( "#numpad-cntnr" );
	$_channum = $( "#npad-channum-txt" );
	var dkey_dash = '.';

	$_btn_ary = new Array ( $("#npad-btn-0"), $("#npad-btn-1"), $("#npad-btn-2"), $("#npad-btn-3"), $("#npad-btn-4"), $("#npad-btn-5"), $("#npad-btn-6"), $("#npad-btn-7"), $("#npad-btn-8"), $("#npad-btn-9"), $("#npad-btn-clear"), $("#npad-btn-enter"), $("#npad-btn-chup"), $("#npad-btn-chdn"), $("#npad-btn-dash") );

	for( var bx = 0; bx < $_btn_ary.length; bx++ )
	{
		$_btn_ary[bx].click( function()
		{
			var dkey = $(this).data("key");
			if( ((dkey >= "0") && (dkey <= "9")) || (dkey == dkey_dash) )
			{
				if( text_is_volatile )
					channum = "";
				text_is_volatile = false;

				if (channum.length < 5 )
				{
					if( dkey == dkey_dash )
					{
						if( (channum.length > 0) && (channum.indexOf( dkey ) === -1) )
							channum += dkey;
					} else
					{
						channum += dkey;
					}
					numpad_channelnumber_set( channum );
				}

			} else if( dkey == "49" )           // CLEAR
			{
				numpad_channelnumber_set( "" );

			} else if( dkey == "13" )           // ENTER
			{
				if( channum.length > 0)
					fn_channel( channum );
				text_is_volatile = true;
				if( close_on_enter )
					$_btn_exit.click();

			} else if( dkey == "+" )            // CH UP
			{
				fn_channel( "+" );
			} else if( dkey == "-" )            // CH DOWN
			{
				fn_channel( "-" );
			}
			return false;
		} )
		.mouseenter( function() { _mouseenter( $(this) ); return false; } )
		.mouseleave( function() { _mouseleave( $(this) ); return false; } )
		.mousedown(  function() { _mousedown( $(this) );  return false; } )
		.mouseup(    function() { _mouseup( $(this) );    return false; } );
	}//for bx

	$_btn_exit = $( "#npad-btn-x" )				// EXIT
		.click( function() { _numpad_hide(); fn_exit(); return false; } )
		.mouseenter( function() { $(this).css( "cursor", "pointer" );  return false; } )
		.mouseleave( function() { vdest_css_cursor_default( $(this) ); return false; } )
		.mousedown(  function() { _mousedown( $(this) );               return false; } )
		.mouseup(    function() { _mouseup( $(this) );   npad_effect_set( $(this), null ); return false; } );

	if( os1_ie_uglify() )
		$( "#npad-chn-win" ).removeClass( "npad-chn-win-bkg" ).addClass( "npad-chn-win-bkg-ie" );

}// _create()


function npad_mouseclick_emul( $o )
{
	$o.mousedown().click();
	setTimeout( function()
	{
		$o.mouseup();
		npad_effect_set( $o, null );
	}, 40 );
}

function numpad_keyup( evt )
{
	if( $_numpad.is(":visible") )
	{
		switch( evt.keyCode )
		{
			case 27/*escape*/:  npad_mouseclick_emul( $_btn_exit ); break;// Close the source selection pop-up if the escape key was pressed
			case 13/*enter*/:   npad_mouseclick_emul( $_btn_ary[11] ); break;
			case 67/*C*/:       npad_mouseclick_emul( $_btn_ary[10] ); break;
			case 190/*.*/:
			case 46/*del.*/:    npad_mouseclick_emul( $_btn_ary[14] ); break;
			case 107/*num+*/:
			case 61/*+*/:       npad_mouseclick_emul( $_btn_ary[12] ); break;
			case 109/*num-*/:
			case 173/*-*/:	    npad_mouseclick_emul( $_btn_ary[13] ); break;
			case 45/*num0*/:
			case 48/*0*/:	    npad_mouseclick_emul( $_btn_ary[0] ); break;
			case 35/*num1*/:
			case 49/*1*/:	    npad_mouseclick_emul( $_btn_ary[1] ); break;
			case 40/*num2*/:
			case 50/*2*/:	    npad_mouseclick_emul( $_btn_ary[2] ); break;
			case 34/*num3*/:
			case 51/*3*/:	    npad_mouseclick_emul( $_btn_ary[3] ); break;
			case 37/*num4*/:
			case 52/*4*/:	    npad_mouseclick_emul( $_btn_ary[4] ); break;
			case 12/*num5*/:
			case 53/*5*/:	    npad_mouseclick_emul( $_btn_ary[5] ); break;
			case 39/*num6*/:
			case 54/*6*/:	    npad_mouseclick_emul( $_btn_ary[6] ); break;
			case 36/*num7*/:
			case 55/*7*/:	    npad_mouseclick_emul( $_btn_ary[7] ); break;
			case 38/*num8*/:
			case 56/*8*/:	    npad_mouseclick_emul( $_btn_ary[8] ); break;
			case 33/*num9*/:
			case 57/*9*/:	    npad_mouseclick_emul( $_btn_ary[9] ); break;
			case 16/*Shft*/:    break;
			default:	//alert( "(np)key: " + evt.keyCode );
		}
	}
}//_keyup()


var npad_posn = { hide:{ top:0, left:0 }, show:{ top:0, left:0 } };

function numpad_size_set( height ) { $_numpad.height( height ).width( height * (500/768) ); } // dimensions of the image

function numpad_size_and_offset_set( height, l_top, l_left )
{
	numpad_size_set( height );

		// Since I had to wrap the channel number window in a div for IE7, it has to be sized dynamically
	var hei = height * 0.095;
	var wid = (278.0/128.0) * hei; // dimensions of image
	$( "#npad-chn-win" ).height( hei ).width( wid );
	$( "#npad-channum-txt" ).css( { fontSize:height * 0.050 } );

	npad_posn.show = { top:l_top, left:l_left };
	$_numpad.css( { top:l_top, left:l_left } ); // use css to locate, .offset() doesn't work on hidden elements
}

function numpad_size_and_offset_set_center( height, height_cntnr )
{
	numpad_size_set( height );
	numpad_size_and_offset_set( height, ((height_cntnr - $_numpad.height()) / 2), (($("body" ).width() - $_numpad.width()) / 2) );
}

function numpad_show( current_channel, is_volatile, close_enter, offset )
{
	if( typeof( is_volatile ) === 'undefined' )
		is_volatile = true;
	if( typeof( close_enter ) === 'undefined' )
		close_enter = true;

	numpad_channelnumber_set( current_channel );

	text_is_volatile = is_volatile;
	close_on_enter = close_enter;
	npad_posn.hide = offset;
	os1_popup_show( $_numpad, 300, npad_posn.hide, npad_posn.show );
}

function _numpad_hide()
{
	os1_popup_hide( $_numpad, 300, npad_posn.hide );
}
