-- two players and one ball
playerLeft = { x = 50, y = 100, speed = 150, img = nil }
playerRight = { x = 720, y = 200, speed = 150, img = nil }
ball = { x = 400, y = 300, speedX = 150, speedY = 150, img = nil }

-- load assets
function love.load(arg)
  playerLeft.img = love.graphics.newImage('assets/paddle-blue.png') 
  playerRight.img = love.graphics.newImage('assets/paddle-green.png') 
  ball.img = love.graphics.newImage('assets/ball.png')
  courtImg = love.graphics.newImage('assets/court.png')
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

  -- ball movements
  if ball.x < 0 or ball.x > love.graphics.getWidth() - ball.img:getWidth()  then
    ball.speedX = -1*ball.speedX
  end

  if ball.y < 0 or ball.y > love.graphics.getHeight() - ball.img:getHeight()  then
    ball.speedY = -1*ball.speedY
  end


  ball.x = ball.x + ball.speedX*dt
  ball.y = ball.y + ball.speedY*dt

end

-- redraw the screen
function love.draw(dt)

  love.graphics.draw(courtImg, 0,0 )
  love.graphics.draw(ball.img, ball.x, ball.y)
  love.graphics.draw(playerLeft.img, playerLeft.x, playerLeft.y)
  love.graphics.draw(playerRight.img, playerRight.x, playerRight.y)

end

-- basic checking for collisions
function CheckCollision(x1,y1,w1,h1, x2,y2,w2,h2)
  return x1 < x2+w2 and
         x2 < x1+w1 and
         y1 < y2+h2 and
         y2 < y1+h1
end
