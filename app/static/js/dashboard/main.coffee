jQuery ->

  class DataView extends Backbone.View
    el: $ "body"

    initialize: ->
      _.bindAll @, 'weeklyDelta', 'drawNumber'
      @model.on "change", @render, @
      @render()
      @model.update()

    weeklyDelta: ->
      (@model.get('weeklyUsage') - @model.get('weeklyAverage')) / @model.get('weeklyAverage')

    drawNumber: (element, number, type='percentage', decimals=2) ->
      if type == 'percentage'
        multiplier = 100
      else if type == 'dollar'
        multiplier = 1
      else
        multiplier = 1

      number *= multiplier
      
      # text before the number
      text = ""
      if type == 'dollar'
        text += "$"

      # the number
      text += Math.abs(number).toFixed(2)

      # text after the number, and adding css class
      if type == 'percentage'
        text += "%"
      if type == 'percentage'
        text += " "
        console.log("number is", number)
        if number < 0 
          element.addClass "good"
          element.removeClass "bad"
        else
          element.addClass "bad"
          element.removeClass "good"
        text += if number > 0 then "more" else "less"
      if type == 'dollar'
        element.addClass 'neutral'

      element.text text

    render: ->
      yesterdayUsage = @model.get('yesterdayUsage')
      dailyAverage = @model.get('dailyAverage')
      weeklyUsage = @model.get('weeklyUsage')
      weeklyAverage = @model.get('weeklyAverage')
      @drawNumber($("#today-use"), @model.get('todaySoFar'), "dollar")
      @drawNumber($("#yesterday-delta"), (yesterdayUsage - dailyAverage) / dailyAverage)
      @drawNumber($("#weekly-delta"), (weeklyUsage - weeklyAverage) / weeklyAverage)
      @drawNumber($("#sleeping-use"), @model.get('sleepingUsage'), 'dollar')


  class DataModel extends Backbone.Model

    initialize: ->
      _.bindAll @, 'update'

    defaults: ->
      todaySoFar: 0
      yesterdayUsage: 0
      dailyAverage: 0
      weeklyUsage: 0
      weeklyAverage: 0
      sleepingUsage: 0

    update: ->
      model = @
      $.getJSON '/data/dashboard', (data) ->
        console.log "update"
        console.log data
        model.set('todaySoFar', data.todaySoFar)
        model.set('yesterdayUsage', data.yesterdayUsage)
        model.set('dailyAverage', data.dailyAverage)
        model.set('weeklyUsage', data.weeklyUsage)
        model.set('weeklyAverage', data.weeklyAverage)
        model.set('sleepingUsage', data.sleepingUsage)


  dataView = new DataView model: new DataModel

