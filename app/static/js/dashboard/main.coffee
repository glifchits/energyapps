jQuery ->

  class DataView extends Backbone.View
    el: $ '#week-usage'

    initialize: =>
      @render()

    render: =>
      $(@el).html "<b>#{@model.get('weekUsage')}</b>"


  class DataModel extends Backbone.Model

    defaults:
      weekUsage: 0


  dataView = new DataView model: new DataModel

