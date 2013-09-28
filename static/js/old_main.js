(function($, window, document, undefined) {

var fRoll = {

	currentStep: 0,
	stepNumber: 4,

	isAnimating: false,


	BreadCrumbEl: $('#breadcrumb'),
	StepsEl: $('#steps > li'),

	initBreadCrumb: function(){
		var b_width = this.BreadCrumbEl.width();

		for(var i=0; i<this.stepNumber; i++){
			var bullet = $('<span />').css({
				left: 100*i/(this.stepNumber-1)+'%'
			})

			if(i == 0){
				bullet.addClass('current');
			}

			bullet.appendTo( this.BreadCrumbEl );
		}
	},

	goNext: function(){
		this.jumpTo( this.currentStep + 1);
	},

	getStep: function(n){
		return this.StepsEl.eq(n);
	},

	jumpTo: function(newStep){
		if(this.isAnimating) return;

		var self = this;
		this.isAnimating = true;

		var out_effect = ( newStep > this.currentStep ) ? 'moveToLeftFade' : 'moveToRightFade',
		    in_effect  = ( newStep > this.currentStep ) ? 'moveFromRightFade': 'moveFromLeftFade';


	    this.getStep( this.currentStep )
	        .addClass( out_effect )
	        .on( 'webkitAnimationEnd', function(){

	            $(this).off( 'webkitAnimationEnd' );
	            $(this).removeClass( out_effect+" current" );

	            self.isAnimating = false;
	    });

	    this.getStep( newStep )
	        .addClass( in_effect )
	        .on( 'webkitAnimationEnd', function(){

	            $(this).off( 'webkitAnimationEnd' );
	            $(this).removeClass( in_effect );

	            self.isAnimating = false;
	    });

	    this.getStep( newStep ).addClass( 'current' );    
	    this.currentStep = newStep;

		    //this.r3_set_paging(newSlide);
	}, 

	normalize: function(x, istart, istop, ostart, ostop){
		return ostart + (ostop - ostart) * ((x - istart) / (istop - istart));
	}
};


fRoll.initBreadCrumb();

$("#steps").on('click', function(){
	fRoll.goNext()
})

})(jQuery, window, document);