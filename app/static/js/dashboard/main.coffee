jQuery ->

  class DataView extends Backbone.View
    el: $ "body"
    yesterday: $ "#yesterday-delta"
    weekly: $ "#weekly-delta"
    sleeping: $ "#sleeping-use"

    initialize: ->
      _.bindAll @, 'yesterdayDelta', 'weeklyDelta', 'drawNumber'
      @render()

    yesterdayDelta: ->
      (@model.get('yesterdayUsage') - @model.get('dailyAverage')) / @model.get('dailyAverage')

    weeklyDelta: ->
      (@model.get('weeklyUsage') - @model.get('weeklyAverage')) / @model.get('weeklyAverage')

    drawNumber: (element, number, type='percentage', decimals=2) ->
      if type == 'percentage'
        multiplier = 100
      else if type == 'dollar'
        multiplier = 1
      else
        multiplier = 1

      number = (number * multiplier).toFixed(decimals)
      
      # text before the number
      text = ""
      if type == 'dollar'
        text += "$"

      # the number
      text += Math.abs(number)

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
      @drawNumber(@yesterday, @yesterdayDelta())
      @drawNumber(@weekly, @weeklyDelta())
      @drawNumber(@sleeping, @model.get('sleepingUsage'), 'dollar')


  class DataModel extends Backbone.Model

    defaults:
      yesterdayUsage: 20
      weeklyUsage: 150
      dailyAverage: 19.4
      weeklyAverage: 152.2
      sleepingUsage: 1.25


  dataView = new DataView model: new DataModel

  console.log dataView

