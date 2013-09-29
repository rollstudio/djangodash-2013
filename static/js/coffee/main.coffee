class fRoll
	constructor: ->
		@currentStep = 0
		@stepNumber = 4
		@isAnimating = false

		@BreadCrumbEl = $('#breadcrumb')
		@BreadCrumbProgress = @BreadCrumbEl.find '.progress'

		@StepsEl = $('#steps > li')

		@init()

	init: ->
		@StepsEl.filter('#intro').find('select').select2()

	initBreadCrumb: ->
		b_width = @BreadCrumbEl.width()

		for i in [0..@stepNumber-1]
			bullet = $('<span />').css left: "#{100*i/(@stepNumber-1)}%"
			bullet.addClass 'done current' if i == 0
			bullet.appendTo @BreadCrumbEl

	progressBreadCrumb: (step_number) ->
		bullet_step = @BreadCrumbEl.find('span').eq(step_number)
		
		@BreadCrumbEl.find('span').removeClass 'current'
		bullet_step.addClass 'current'

		@BreadCrumbProgress.animate width: bullet_step[0].style.left, 500, ->
			bullet_step.addClass 'done'
			


	goNext: ->
		@jumpTo( @currentStep + 1 )

	getStep: (n) ->
		@StepsEl.eq n

	jumpTo: (newStep) ->
		return false if @isAnimating
		return false if newStep > @stepNumber-1
		self = @
		@isAnimating = true

		@progressBreadCrumb newStep

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


$('a.next').on 'click', ->
	roll.goNext()

