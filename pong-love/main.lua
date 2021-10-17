-- two players and one ball
playerLeft = { x = 50, y = 100, speed = 150, img = nil }
playerRight = { x = 720, y = 200, speed = 150, img = nil }
ball = { x = 400, y = 300, speed = 150, img = nil }

-- load assets
function love.load(arg)
  playerLeft.img = love.graphics.newImage('assets/paddle-blue.png') 
  playerRight.img = love.graphics.newImage('assets/paddle-green.png') 
  ball.img = love.graphics.newImage('assets/ball.png')
end

-- main functionality
function love.update(dt)

  -- exit the game
  if love.keyboard.isDown('escape', 'q') then
    love.event.push('quit')
  end

  -- players actions
  if love.keyboard.isDown('w') then
    if playerLeft.y > 0 then
      playerLeft.y = playerLeft.y - (playerLeft.speed*dt)
    end
  end

  if love.keyboard.isDown('s') then
    if playerLeft.y + playerLeft.img:getHeight() < love.graphics.getHeight() then
      playerLeft.y = playerLeft.y + (playerLeft.speed*dt)
    end
  end

  if love.keyboard.isDown('up') then
    if playerRight.y > 0 then
      playerRight.y = playerRight.y - (playerRight.speed*dt)
    end
  end

  if love.keyboard.isDown('down') then
    if playerRight.y + playerRight.img:getHeight() < love.graphics.getHeight() then
      playerRight.y = playerRight.y + (playerRight.speed*dt)
    end
  end

end

-- redraw the screen
function love.draw(dt)
  love.graphics.draw(ball.img, ball.x, ball.y)
  love.graphics.draw(playerLeft.img, playerLeft.x, playerLeft.y)
  love.graphics.draw(playerRight.img, playerRight.x, playerRight.y)

end
