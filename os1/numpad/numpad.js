/* Number pad popup. Requires jquery.
*/

var $_btn_ary;
var $_btn_exit;
var $_numpad = null;
var $_channum = null;
var channum = "";
var text_is_volatile = true;
var close_on_enter = true;


function numpad_channelnumber_set( new_chnn )
{
	channum = new_chnn;
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
	$o.css( "cursor", "pointer" );
	npad_effect_set( $o, "numpad-effect-hover" );
}
function _mouseleave( $o )
{
	$o.css( "cursor", "default" );
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
				<div id="npad-chnn"      class="npad-btn-brdr numpad-bkg"><span id="npad-channum-txt">0</span></div>\
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
	$_channum.html( channum );
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
					$_channum.html( channum );
				}

			} else if( dkey == "49" )           // CLEAR
			{
				channum = "";
				$_channum.html( channum );

			} else if( dkey == "13" )           // ENTER
			{
				if( channum.length > 0)
					fn_channel( channum );
				text_is_volatile = true;
				if( close_on_enter )
					$_btn_exit.click();

			} else if( (dkey == "+") || (dkey == "-") )            // CH UP, DOWN
			{
				if( channum.length > 0 )
				{
					var ichan;
					var ss = channum.split( dkey_dash );
					if( ss.length > 1 )
						ichan = parseInt( ss[1] );
					else ichan = parseInt( channum );

					if( dkey == "+" ) // CH UP
					{
						if( ichan < 9999 )
							ichan++;
					fn_channel( "+" );
					} else if( dkey == "-" ) // CH DOWN
					{
						if( ichan > 0 )
							ichan--;
					fn_channel( "-" );
					}

					if( ss.length > 1 )
						channum = ss[0] + dkey_dash + ichan.toString();
					else channum = ichan.toString();

					$_channum.html( channum );
				}
			}
			return false;
		} ).mouseenter( function()
		{
			_mouseenter( $(this) );
			return false;
		} ).mouseleave( function()
		{
			_mouseleave( $(this) );
			return false;
		} ).mousedown( function()
		{
			_mousedown( $(this) );
			return false;
		} ).mouseup( function()
		{
			_mouseup( $(this) );
			return false;
		} );
	}//for bx

	$_btn_exit = $( "#npad-btn-x" ).click( function()   // EXIT
	{
		$_numpad.hide( os1_nav_is_mobile ? 0 : 300 );
		fn_exit();
		return false;
	} ).mousedown( function()
	{
		_mousedown( $(this) );
		return false;
	} ).mouseup( function()
	{
		_mouseup( $(this) );
		npad_effect_set( $(this), null );
		return false;
	} );

	$_numpad.hide();

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
			default:	alert( "(np)key: " + evt.keyCode );
		}
	}
}//_keyup()

function numpad_size_set( height )
{
	$_numpad.height( height );
	$_numpad.width( height / 1.542 );
	$_channum.css( "font-size", height * 0.050 );

		// Since I had to wrap the channel number window in a div for IE7, it has to be sized dynamically
	var hei = height * 0.095;
	var wid = (278.0/128.0) * hei; // dimensions of image
	$( "#npad-chnn" ).height( hei ).width( wid );
}

var numpad_posn_calc;
var channum_posn_calc;

function numpad_position_center( par_top, par_left, par_height, par_width )
{
	numpad_posn_calc = { top:par_top + ((par_height - $_numpad.height()) / 2), left:par_left + ((par_width - $_numpad.width()) / 2) };
	$_numpad.offset( numpad_posn_calc );

		// The location of text in the window drops as the size of the numpad gets smaller. Fixitinscript.
	var channum_posn_calc = { top:numpad_posn_calc.top + ($_numpad.height() * 0.090), left:numpad_posn_calc.left + ($_numpad.width() * 0.180) };
	if( $_channum.is( ":visible" ) )
		$_channum.offset( channum_posn_calc );
}

function numpad_show( is_volatile, close_enter )
{
	if( typeof( is_volatile ) === 'undefined' )
		is_volatile = true;
	if( typeof( close_enter ) === 'undefined' )
		close_enter = true;

	text_is_volatile = is_volatile;
	close_on_enter = close_enter;
	$_numpad.show( os1_nav_is_mobile ? 0 : 300, function()
	{
			// After a screen resize jquery doesn't reset the offset properly when the pop-up is hidden. This re-centers it.
		$_numpad.offset( numpad_posn_calc );
		$_channum.offset( channum_posn_calc );
	});
}