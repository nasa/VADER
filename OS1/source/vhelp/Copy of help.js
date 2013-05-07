/* Help overlay. Requires jquery.
*/

var $_help = null;
var $_div_ary;
var $_help_btn_exit;

var help_is_showing_sgl = false;
var help_is_showing_mlt = false;
var help_is_showing_pwr = false;
var help_is_showing_dflt = false;
var help_is_showing_chn = false;
function help_is_showing_subpup() { return (help_is_showing_sgl || help_is_showing_mlt || help_is_showing_pwr || help_is_showing_dflt || help_is_showing_chn); }



function help_effect_set( $o, new_class )
{
	if( $o )
	{
		$o.removeClass( "help-effect-none help-effect-click help-effect-hover" );
		if( new_class )
			$o.addClass( new_class );
	}
}

function help_menter( $o )
{
	vdest_css_cursor_pointer( $o );
	help_effect_set( $o.find(".help-info-item"), "help-effect-hover" ); // Cant get the effect to work on the $o div, so apply it only to the text
}
function help_mleave( $o )
{
	vdest_css_cursor_default( $o );
	help_effect_set( $o.find(".help-info-item"), null );
}
function help_mdown( $o )
{
	help_effect_set( $o.find(".help-info-item"), "help-effect-click" );
	$o.css( "opacity", 0.3 );
}
function help_mup( $o )
{
	help_effect_set( $o.find(".help-info-item"), "help-effect-hover" );
	$o.css( "opacity", 1.0 );
}

// Generate the html for numpad
function help_create( fn_exit )
{
	$(document.body).append('\
		<div id="help-cntnr-mn" class="help-cntnr help-bkg">\
			<img id="help-btn-x"  class="help-btn-brdr" src="help/img/help-btn-x.png">\
			<div class="help-title help-bkg"><i><span style="font-size:larger;">A</span>bout the <span style="font-size:larger;">D</span>isplay <span style="font-size:larger;">C</span>ontrol...</i></div>\
			<div class="help-info-cntnr">\
				<img class="info-icon newln" src="help/img/help-info-lg.png">\
				<div class="help-info-intro">\
					The purpose of this tool is to direct the any of the eight video input sources to any one of the eight output devices that are shown on this \
					page. The output devices consist of six televisions and two MCC High-End-Video System ports. Click on the following capabilities for more information:\
				</div>\
				<div id="h-cap-input-single" class="newln indent">\
					<img src="help/img/help-btn-ptr.png">\
					<span class="help-info-item help-cap-bkg">Select a source input for, or control an output,</span>\
				</div>\
				<div id="h-cap-input-multi" class="newln indent">\
					<img src="help/img/help-btn-ptr.png">\
					<span class="help-info-item help-cap-bkg">Select a source input for, or control multiple outputs,</span>\
				</div>\
				<div id="h-cap-power" class="newln indent">\
					<img src="help/img/help-btn-ptr.png">\
					<span class="help-info-item help-cap-bkg">Power toggle the output,</span>\
				</div>\
				<div id="h-cap-default" class="newln indent">\
					<img src="help/img/help-btn-ptr.png">\
					<span class="help-info-item help-cap-bkg">Reset outputs to their default configuration,</span>\
				</div>\
				<div id="h-cap-tvchan" class="newln indent">\
					<img src="help/img/help-btn-ptr.png">\
					<span class="help-info-item help-cap-bkg">Change the channel of the Cable-TV input source.</span>\
				</div>\
			</div>\
		</div>');

	$_help = $( "#help-cntnr-mn" );

	$_div_ary = new Array ( $( "#h-cap-input-single" ), $( "#h-cap-input-multi" ), $( "#h-cap-power" ), $( "#h-cap-default" ), $( "#h-cap-tvchan" ) );

	for( var bx = 0; bx < $_div_ary.length; bx++ )
	{
		$_div_ary[bx].mousedown( function()
		{
			help_mdown( $(this) );
			return false;
		} ).mouseup( function()
		{
			help_mup( $(this) );
			return false;
		} );
	}//for bx

	$_div_ary[0].click( function()              // OUTPUT SINGLE SELECT
	{
		help_sgl_create( function()//exit sgl
		{
			help_is_showing_sgl = false;
			$_help.show();
			$_vdestinations[3].removeClass( "help-vdest-effect-bigger" );
		} );
		for( var bx = 0; bx < $_div_ary.length; bx++ )
			help_mleave( $_div_ary[bx] );
		help_is_showing_sgl = true;
		help_sgl_size_and_offset_set();
		help_hide();
		help_sgl_show();
		for( var dx = 0; dx < $_vdestinations.length-2; dx++ )
			$_vdestinations[dx].removeClass( "help-vdest-effect-bigger" );
		$_vdestinations[3].addClass( "help-vdest-effect-bigger" );
		return false;
	} ).mouseenter( function()
	{
		if( !help_is_showing_sgl )
		{
			help_menter( $(this) );
			for( var dx = 0; dx < $_vdestinations.length; dx++ )
				$_vdestinations[dx].addClass( "help-vdest-effect-bigger" );
		}
		return false;
	} ).mouseleave( function()
	{
		if( !help_is_showing_sgl )
		{
			help_mleave( $(this) );
			for( var dx = 0; dx < $_vdestinations.length; dx++ )
				$_vdestinations[dx].removeClass( "help-vdest-effect-bigger" );
		}
		return false;
	} );

	$_div_ary[1].click( function()              // CHECKBOX MULTI SELECT
	{
		help_mlt_create( function()//exit mlt
		{
			help_is_showing_mlt = false;
			$_help.show();
			vdest_cbox_uncheck( $_vdestinations[0], null );
			vdest_cbox_uncheck( $_vdestinations[2], null );
			vdest_cbox_uncheck( $_vdestinations[4], null );
			$_vdest_btn_selected.removeClass( "help-vdest-effect-bigger" );
			vdest_btn_selected_hide();
		} );
		for( var bx = 0; bx < $_div_ary.length; bx++ )
			help_mleave( $_div_ary[bx] );
		help_is_showing_mlt = true;
		help_mlt_size_and_offset_set();
		help_hide();
		help_mlt_show();
		for( var dx = 0; dx < $_vdestinations.length; dx++ )
			$_vdestinations[dx].find( ".vdest-tvbtn-cbox" ).attr( "src", "img/cbox_clr.png" );
		vdest_cbox_check( $_vdestinations[0], null );
		vdest_cbox_check( $_vdestinations[2], null );
		vdest_cbox_check( $_vdestinations[4], null );
		vdest_btn_selected_show();
		$_vdest_btn_selected.addClass( "help-vdest-effect-bigger" );
		return false;
	} ).mouseenter( function()
	{
		if( !help_is_showing_mlt )
		{
			help_menter( $(this) );
			for( var dx = 0; dx < $_vdestinations.length; dx++ )
				$_vdestinations[dx].find( ".vdest-tvbtn-cbox" ).attr( "src", "img/cbox_chk.png" );
		}
		return false;
	} ).mouseleave( function()
	{
		if( !help_is_showing_mlt )
		{
			help_mleave( $(this) );
			for( var dx = 0; dx < $_vdestinations.length; dx++ )
				$_vdestinations[dx].find( ".vdest-tvbtn-cbox" ).attr( "src", "img/cbox_clr.png" );
		}
		return false;
	} );

	$_div_ary[2].click( function()              // POWER TOGGLE
	{
		help_pwr_create( function()//exit pwr
		{
			help_is_showing_pwr = false;
			$_help.show();
			$_vdestinations[5].find( ".vdest-tvbtn-power" ).removeClass( "help-vdest-effect-bigger" );
		} );
		for( var bx = 0; bx < $_div_ary.length; bx++ )
			help_mleave( $_div_ary[bx] );
		help_is_showing_pwr = true;
		help_pwr_size_and_offset_set();
		help_hide();
		help_pwr_show();
		for( var dx = 0; dx < $_vdestinations.length-2; dx++ )
			$_vdestinations[dx].find( ".vdest-tvbtn-power" ).removeClass( "help-vdest-effect-bigger" );
		$_vdestinations[5].find( ".vdest-tvbtn-power" ).addClass( "help-vdest-effect-bigger" );
		return false;
	} ).mouseenter( function()
	{
		if( !help_is_showing_pwr )
		{
			help_menter( $(this) );
			for( var dx = 0; dx < $_vdestinations.length-2; dx++ )
				$_vdestinations[dx].find( ".vdest-tvbtn-power" ).addClass( "help-vdest-effect-bigger" );
		}
		return false;
	} ).mouseleave( function()
	{
		if( !help_is_showing_pwr )
		{
			help_mleave( $(this) );
			for( var dx = 0; dx < $_vdestinations.length-2; dx++ )
				$_vdestinations[dx].find( ".vdest-tvbtn-power" ).removeClass( "help-vdest-effect-bigger" );
		}
		return false;
	} );

	$_div_ary[3].click( function()              // DEFAULT SETUP
	{
		for( var bx = 0; bx < $_div_ary.length; bx++ )
			help_mleave( $_div_ary[bx] );
		return false;
	} ).mouseenter( function()
	{
		help_menter( $(this) );
		$( ".vdest-btn-default" ).addClass( "help-vdest-effect-bigger" );
		return false;
	} ).mouseleave( function()
	{
		help_mleave( $(this) );
		$( ".vdest-btn-default" ).removeClass( "help-vdest-effect-bigger" );
		return false;
	} );

	$_div_ary[4].click( function()              // CHANGE CHANNEL
	{
		for( var bx = 0; bx < $_div_ary.length; bx++ )
			help_mleave( $_div_ary[bx] );
		return false;
	} ).mouseenter( function()
	{
		help_menter( $(this) );
		$( ".vdest-btn-numpad" ).addClass( "help-vdest-effect-bigger" );
		return false;
	} ).mouseleave( function()
	{
		help_mleave( $(this) );
		$( ".vdest-btn-numpad" ).removeClass( "help-vdest-effect-bigger" );
		return false;
	} );

	$_help_btn_exit = $( "#help-btn-x" ).click( function()   // EXIT
	{
			// clear off any residual effects
		for( var dx = 0; dx < $_vdestinations.length; dx++ )
		{
			$_vdestinations[dx].removeClass( "help-vdest-effect-bigger" );
			$_vdestinations[dx].find( ".vdest-tvbtn-cbox" ).attr( "src", "img/cbox_clr.png" );
			$_vdestinations[dx].find( ".vdest-tvbtn-power" ).removeClass( "help-vdest-effect-bigger" );
		}
		$( ".vdest-btn-default" ).removeClass( "help-vdest-effect-bigger" );
		$( ".vdest-btn-numpad" ).removeClass( "help-vdest-effect-bigger" );

		help_hide( os1_is_small_device() ? 0 : 300 );
		fn_exit();
		return false;
	} ).mouseenter( function()
	{
		$(this).css( "cursor", "pointer" );
		return false;
	} ).mouseleave( function()
	{
		vdest_css_cursor_default( $(this) );
		return false;
	} ).mousedown( function()
	{
		help_mdown( $(this) );
		return false;
	} ).mouseup( function()
	{
		help_mup( $(this) );
		help_effect_set( $(this), null );
		return false;
	} );

//	help_hide();

}// _create()


function help_mouseclick_emul( $o )
{
	$o.mousedown().click();
	setTimeout( function()
	{
		$o.mouseup();
		help_effect_set( $o, null );
	}, 40 );
}

function help_keyup( evt )
{
	if( evt.keyCode === 27/*escape*/ )
	{
		if( $_help.is(":visible") )
			help_mouseclick_emul( $_help_btn_exit );
		else if( help_is_showing_sgl )
			help_mouseclick_emul( $_help_sgl_btn_exit );
		else if( help_is_showing_mlt )
			help_mouseclick_emul( $_help_mlt_btn_exit );
	}
}//_keyup()


var font_size;
var font_size_title;

function $_help_size_and_offset_set( $o, height, proportions, l_top, l_left )
{
	if( $o )
	{
		$o.height( height );
		$o.width( height * proportions ); // ratio of the dimensions of the img
		$o.css( "font-size", font_size );
		$o.find( ".help-title" ).css( "font-size", font_size_title );
		$o.css( { top:l_top, left:l_left } );
	}
}

var hlp_posn_final;
var hlp_posn_sgl;
var hlp_posn_mlt;
var hlp_posn_chn;
var hlp_posn_dflt;
var hlp_posn_pwr;
var hlp_height_max;
var hlp_posn_orig = { top:0, left:0 };


function help_size_and_offset_set( height, l_top, l_left )
{
	font_size = height * 0.0480;
	font_size_title = height * 0.070;
	hlp_posn_final = { top:l_top, left:l_left };
	$_help_size_and_offset_set( $_help, height, (876/512), l_top, l_left );
	hlp_height_max = height;
	hlp_posn_sgl  = { top:l_top, left:l_left/2 };
	help_sgl_size_and_offset_set();
	hlp_posn_mlt  = { top:l_top, left:l_left/32 };
	help_mlt_size_and_offset_set();
	hlp_posn_pwr  = { top:l_top + (height/4), left:l_left };
	help_pwr_size_and_offset_set();
	hlp_posn_chn  = { top:l_top + (height/8), left:l_left/4 };
	hlp_posn_dflt = { top:l_top + (height/8), left:l_left/4 };
}

function help_show( offset )
{
	hlp_posn_orig = offset;
	os1_popup_show( $_help, 400, hlp_posn_orig, hlp_posn_final );
}

function help_hide()
{
	os1_popup_hide( $_help, 400, hlp_posn_orig );
}


/**************************** SINGLE SELECTED POPUP
										 ****************************/
var $_help_sgl = null;
var $_help_sgl_btn_exit;

function help_sgl_create( fn_exit )
{
	$(document.body).append('\
		<div id="help-cntnr-sgl" class="help-cntnr help-bkg">\
			<img id="help-sgl-x"  class="help-btn-brdr" src="help/img/help-btn-x.png">\
			<div class="help-title help-bkg"><i><span style="font-size:larger;">S</span>ingle <span style="font-size:larger;">O</span>utput <span style="font-size:larger;">S</span>election </i></div>\
			<div class="help-info-cntnr">\
				<img class="info-icon newln" src="help/img/help-info-lg.png">\
				<div class="help-info-intro">\
					When a single Output device has been selected, this <img class="vsrc-icon" src="help/img/vsrc.jpg"> pop-up dialog will be displayed allowing \
					the user to select from one of the Input sources that are shown in the left-hand box. This Input source will then be connected to the Output \
					that is shown on the top of the dialog.<br/>On the right-hand side of the dialog, power and volume buttons that when clicked or touched will \
					perform their respective functions on the Output device.\
				</div>\
				<div id="help-sgl-back" class="newln indent">\
					<span class="help-info-item help-cap-bkg"><= Go Back</span>\
				</div>\
			</div>\
		</div>');

	$_help_sgl = $( "#help-cntnr-sgl" );
	$_help_sgl_btn_exit = $( "#help-sgl-x" );

	$( "#help-sgl-x, #help-sgl-back" )
		.click( function() { $_help_sgl.hide( os1_is_small_device() ? 0 : 300 ); fn_exit(); return false; } )
		.mouseenter( function() { $(this).css( "cursor", "pointer" ); return false; } )
		.mouseleave( function() { vdest_css_cursor_default( $(this) ); return false; } )
		.mousedown( function() { help_mdown( $(this) ); return false; } )
		.mouseup( function() { help_mup( $(this) ); help_effect_set( $(this), null ); return false; } );

	$_help_sgl.hide();
}

function help_sgl_size_and_offset_set()
{
	$_help_size_and_offset_set( $_help_sgl, hlp_height_max, (876/512), hlp_posn_sgl.top, hlp_posn_sgl.left );
}

function help_sgl_show()
{
	$_help_sgl.show( os1_is_small_device() ? 0 : 300 );
}


										/**************************** MULTIPLE SELECTED POPUP
                                        ****************************/
var $_help_mlt = null;
var $_help_mlt_btn_exit;

function help_mlt_create( fn_exit )
{
	$(document.body).append('\
		<div id="help-cntnr-mlt" class="help-cntnr help-bkg">\
			<img id="help-mlt-x"  class="help-btn-brdr" src="help/img/help-btn-x.png">\
			<div class="help-title help-bkg"><i><span style="font-size:larger;">M</span>ultiple <span style="font-size:larger;">O</span>utput <span style="font-size:larger;">S</span>election </i></div>\
			<div class="help-info-cntnr">\
				<img class="info-icon newln" src="help/img/help-info-lg.png">\
				<div class="help-info-intro">\
					<img class="help-arrow" src="help/img/help-arrow-20.png">\
					Clicking on a checkbox in the upper right-hand corner of the Output device allows the user to select more than one device to control. \
					By clicking on the "Process Selected Devices", the Input source control dialog <img class="vsrc-icon" src="help/img/vsrc-mlt.jpg">will \
					pop-up allowing the user to select an Input source to be connected to each of the selected Output devices.<br/>The power and volume \
					buttons will perform their respective functions on each of the selected Output devices.\
				</div>\
				<div id="help-mlt-back" class="newln indent">\
					<span class="help-info-item help-cap-bkg"><= Go Back</span>\
				</div>\
			</div>\
		</div>');

	$_help_mlt = $( "#help-cntnr-mlt" );
	$_help_mlt_btn_exit = $( "#help-mlt-x" );

	$( "#help-mlt-x, #help-mlt-back" )
		.click( function() { $_help_mlt.hide( os1_is_small_device() ? 0 : 300 ); fn_exit(); return false; } )
		.mouseenter( function() { $(this).css( "cursor", "pointer" ); return false; } )
		.mouseleave( function() { vdest_css_cursor_default( $(this) ); return false; } )
		.mousedown( function() { help_mdown( $(this) ); return false; } )
		.mouseup( function() { help_mup( $(this) ); help_effect_set( $(this), null ); return false; } );

	$_help_mlt.hide();
}

function help_mlt_size_and_offset_set()
{
	$_help_size_and_offset_set( $_help_mlt, hlp_height_max, (876/512), hlp_posn_mlt.top, hlp_posn_mlt.left );
}

function help_mlt_show()
{
	$_help_mlt.show( os1_is_small_device() ? 0 : 300 );
}


										/**************************** POWER TOGGLE POPUP
										 ****************************/
var $_help_pwr = null;
var $_help_pwr_btn_exit;

function help_pwr_create( fn_exit )
{
	$(document.body).append('\
		<div id="help-cntnr-pwr" class="help-cntnr help-bkg">\
			<img id="help-pwr-x"  class="help-btn-brdr" src="help/img/help-btn-x.png">\
			<div class="help-title help-bkg"><i><span style="font-size:larger;">P</span>ower <span style="font-size:larger;">T</span>oggle</i></div>\
			<div class="help-info-cntnr">\
				<img class="info-icon newln" src="help/img/help-info.png">\
				<div class="help-info-intro">\
					Click on the power button in the lower right-hand corner of the Output device to toggle the power state of that television device.\
					<img class="help-arrow newln" src="help/img/help-ltarrow.png">\
				</div>\
				<div id="help-pwr-back" class="newln indent">\
					<span class="help-info-item help-cap-bkg"><= Go Back</span>\
				</div>\
			</div>\
		</div>');

	$_help_pwr = $( "#help-cntnr-pwr" );
	$_help_pwr_btn_exit = $( "#help-pwr-x" );

	$( "#help-pwr-x, #help-pwr-back" )
		.click( function() { $_help_pwr.hide( os1_is_small_device() ? 0 : 300 ); fn_exit(); return false; } )
		.mouseenter( function() { $(this).css( "cursor", "pointer" ); return false; } )
		.mouseleave( function() { vdest_css_cursor_default( $(this) ); return false; } )
		.mousedown( function() { help_mdown( $(this) ); return false; } )
		.mouseup( function() { help_mup( $(this) ); help_effect_set( $(this), null ); return false; } );

	$_help_pwr.hide();
}

function help_pwr_size_and_offset_set()
{
	$_help_size_and_offset_set( $_help_pwr, hlp_height_max * 0.60, (876/512), hlp_posn_pwr.top, hlp_posn_pwr.left );
}

function help_pwr_show()
{
	$_help_pwr.show( os1_is_small_device() ? 0 : 300 );
}
