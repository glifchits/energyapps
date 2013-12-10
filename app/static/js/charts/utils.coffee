window.utils = {};

utils.hello = () ->
  "Hello there!"

utils.average = (set) ->
  total = set.reduce (x, y) -> x + y
  total / set.length

utils.max = (set) -> 
  Math.max.apply @, set

# thanks to http://www.paulirish.com/2009/random-hex-color-code-snippets/
utils.randomHex = () ->
  "##{Math.floor(Math.random() * 16777215).toString(16)}"

utils.randomRGB = (alpha = 1) ->
  r = parseInt Math.random() * 255
  g = parseInt Math.random() * 255
  b = parseInt Math.random() * 255
  "rgba(#{r},#{g},#{b},#{alpha})"
