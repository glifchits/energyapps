jQuery ->

  class DataView extends Backbone.View
    el: $ "body"

    initialize: ->
      _.bindAll @, 'weeklyDelta', 'drawNumber'
      @render()

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
        element.addClass if number > 0 then "bad" else "good"
        text += if number > 0 then "more" else "less"
      if type == 'dollar'
        element.addClass 'neutral'

      element.text text

    render: =>
      @model.update()
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
      todaySoFar: 3.40
      yesterdayUsage: 20
      dailyAverage: 19.4
      weeklyUsage: 150
      weeklyAverage: 152.2
      sleepingUsage: 1.25

    update: ->
      model = @
      $.getJSON '/data/dashboard', (data) ->
        console.log data
        model.set('todaySoFar', data.todaySoFar)
        model.set('sleepingUsage', 30)


  dataView = new DataView model: new DataModel

