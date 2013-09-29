class fRoll
	constructor: ->
		@currentStep = 0
		@stepNumber = 0
		@isAnimating = false

		@BreadCrumbEl = $('#breadcrumb')
		@BreadCrumbProgress = @BreadCrumbEl.find '.progress'

		@GeneratorId = undefined
		@Questions = undefined
		@Baking_url = undefined
		@Checking_url = undefined

		@StepsEl = $('#steps > li')

		@init()

	init: ->
		input = @StepsEl.filter('#intro').find('input')

		input.typeahead
			name: 'asda'
			minLength: 0
			local: window.Bakehouse.cookies
			valueKey: 'value'
			template: [
			   '<p class="repo-language">{{language}}</p>',
			   '<p class="repo-name">{{options.project_name}}</p>',
			   '<p class="repo-description">{{description}}</p>'
			].join('')
			engine: Hogan
			selected: (selection) ->
				console.log selection

		input.on 'typeahead:selected typeahead:autocompleted', (e, datum) =>
			@GeneratorId = datum.id


	loadGenerator: ->
		choise = _.where window.Bakehouse.cookies, {id: @GeneratorId}

		return if !choise[0]

		@Baking_url = choise[0].baking_url
		@Questions = choise[0].options

		@stepNumber = _(@Questions).size() + 2
		@initSteps()
		@initBreadCrumb()


	generateProject: ->
		$.ajax
			url: @Baking_url
			dataType: 'json'
			type: 'POST'
			data: @Questions
			beforeSend: (req) ->
				req.setRequestHeader("X-CSRFToken", window.csrftoken);
				console.log 'loading'
			success: (json) =>
				@Checking_url = json.url
				window.check_project = window.setInterval $.proxy(@checkProject, @), 4000


	checkProject: ->
		$.ajax
			url: @Checking_url
			dataType: 'json'
			type: 'GET'
			beforeSend: (req) ->
				req.setRequestHeader("X-CSRFToken", window.csrftoken);
			success: (json) =>
				console.log json
				#if json.status == 'PENDING'


	initSteps: ->
		for key,val of @Questions
			template = "
				<li>
					<h1>#{_(key).humanize()}</h1>
					<input type='text' id='#{key}' value='#{val}'></input>
					<a class='next'>
						<span>
							Next
						</span>
					</a>
				</li>
			"
			@StepsEl.filter('#intro').after( template )


		@StepsEl = $('#steps > li') #update it!


	initBreadCrumb: ->
		b_width = @BreadCrumbEl.width()

		for i in [0..@stepNumber-1]
			bullet = $('<span />').css left: "#{100*i/(@stepNumber-1)}%"
			bullet.addClass 'done current' if i == 0
			bullet.appendTo @BreadCrumbEl

		@BreadCrumbEl.fadeIn()
		@goNext()

	progressBreadCrumb: (step_number) ->
		bullet_step = @BreadCrumbEl.find('span').eq(step_number)
		
		@BreadCrumbEl.find('span').removeClass 'current'
		bullet_step.addClass 'current'

		@BreadCrumbProgress.animate width: bullet_step[0].style.left, 500, ->
			bullet_step.addClass 'done'
			

	goNext: ->
		input = @getStep( @currentStep ).find('input')

		if !input.val() & @currentStep > 0
			input.addClass 'error'
			return;

		input.removeClass 'error'
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
			$(@).off 'webkitAnimationEnd'
			$(@).hide()
			$(@).removeClass "#{out_effect} current"

			self.isAnimating = false
		)

		@getStep( newStep ).addClass(in_effect).on('webkitAnimationEnd', ->
			$(@).off 'webkitAnimationEnd'
			$(@).removeClass in_effect

			self.isAnimating = false
		)

		@getStep(newStep).addClass 'current'
		@currentStep = newStep

		@generateProject() if @currentStep == @stepNumber-1


roll = new fRoll

#roll.stepNumber = 10
#roll.initBreadCrumb()


$(document).on 'click', 'a.next', ->
	roll.goNext()


$('a.start').on 'click', ->
	roll.loadGenerator()
