class fRoll
	constructor: () ->
		@currentStep = 0
		@stepNumber = 4
		@isAnimating = false

		@BreadCrumbEl = $('#breadcrumb')
		@StepsEl = $('#steps > li')

	initBreadCrumb: ->
		b_width = @BreadCrumbEl.width()

		for i in [0..@stepNumber-1]
			bullet = $('<span />').css left: "#{100*i/(@stepNumber-1)}%"
			bullet.addClass 'current' if i == 0
			bullet.appendTo @BreadCrumbEl


	goNext: ->
		@jumpTo( @currentStep + 1 )

	getStep: (n) ->
		@StepsEl.eq n

	jumpTo: (newStep) ->
		return false if @isAnimating
		self = @
		@isAnimating = true

		out_effect = if newStep > @currentStep then 'moveToLeftFade' else 'moveToRightFade'
		in_effect = if newStep > @currentStep then 'moveFromRightFade' else 'moveFromLeftFade'

		@getStep(@currentStep).addClass(out_effect).on('webkitAnimationEnd', ->
			$(@).off 'animationEnd'
			$(@).removeClass "#{out_effect} current"

			self.isAnimating = false
		)

		@getStep( newStep ).addClass(in_effect).on('webkitAnimationEnd', ->
			$(@).off 'animationEnd'
			$(@).removeClass in_effect

			self.isAnimating = false
		)

		@getStep(newStep).addClass 'current'
		@currentStep = newStep


roll = new fRoll
roll.initBreadCrumb()

$('#steps').on 'click', ->
	roll.goNext()