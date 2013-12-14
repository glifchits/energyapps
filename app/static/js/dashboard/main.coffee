jQuery ->

  class DataView extends Backbone.View
    el: $ "body"
    yesterday: $ "#yesterday-delta"
    weekly: $ "#weekly-delta"

    initialize: ->
      _.bindAll @, 'yesterdayDelta', 'weeklyDelta', 'drawDelta'
      @render()

    yesterdayDelta: ->
      (@model.get('yesterdayUsage') - @model.get('dailyAverage')) / @model.get('dailyAverage')

    weeklyDelta: ->
      (@model.get('weeklyUsage') - @model.get('weeklyAverage')) / @model.get('weeklyAverage')

    drawDelta: (element, delta) ->
      delta = (delta * 100).toFixed(2)
      if delta > 0
        console.log 'positive'
        element.text delta + "% more"
        element.addClass "bad"
      else if delta < 0
        element.text delta + "% less"
        element.addClass "good"
      else
        element.text "no more"
        element.addClass "neutral"

    render: =>
      @drawDelta(@yesterday, @yesterdayDelta())
      @drawDelta(@weekly, @weeklyDelta())


  class DataModel extends Backbone.Model

    defaults:
      yesterdayUsage: 20
      weeklyUsage: 150
      dailyAverage: 19.4
      weeklyAverage: 152.2


  dataView = new DataView model: new DataModel

  console.log dataView

