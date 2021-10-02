debug = true

player = { x = 200, y = 710, speed = 150, img = nil}
canShoot = true
canShootTimerMax = 0.2
canShootTimer = canShootTimerMax

bulletImg = nil
bullets = {}

createEnemyTimerMax = 0.4
createEnemyTimer = createEnemyTimerMax
enemyIimg = nil
enemies = {}

function love.load(arg)
  player.img = love.graphics.newImage('assets/plane.png')
  bulletImg = love.graphics.newImage('assets/bullet.png')
  enemyImg = love.graphics.newImage('assets/enemy.png')
end

function love.update(dt)
  canShootTimer = canShootTimer - (1 * dt)
  if canShootTimer < 0 then
    canShoot = true
  end

  if love.keyboard.isDown('escape') then
    love.event.push('quit')
  end

  if love.keyboard.isDown('left', 'a') then
    if player.x > 0 then
      player.x = player.x - (player.speed*dt)
    end
  elseif love.keyboard.isDown('right', 'd') then
    if player.x < (love.graphics.getWidth() - player.img:getWidth()) then
      player.x = player.x + (player.speed*dt)
    end
  end

  if love.keyboard.isDown('space', 'rctrl', 'lctrl') and canShoot then
    newBullet = { x = player.x + (player.img:getWidth()/2), y = player.y, img = bulletImg }
    table.insert(bullets, newBullet)
    canShoot = false
    canShootTimer = canShootTimerMax
  end

 for i, bullet in ipairs(bullets) do
   bullet.y = bullet.y - (250*dt)
   if bullet.y < 0 then
     table.remove(bullets, i)
   end
 end

  createEnemyTimer = createEnemyTimer - (1 * dt)
  if createEnemyTimer < 0 then
	  createEnemyTimer = createEnemyTimerMax
	  randomNumber = math.random(10, love.graphics.getWidth() - 10)
	  newEnemy = { x = randomNumber, y = -10, img = enemyImg }
	  table.insert(enemies, newEnemy)
  end

  for i, enemy in ipairs(enemies) do
  	enemy.y = enemy.y + (200 * dt)
  
  	if enemy.y > 850 then -- remove enemies when they pass off the screen
  		table.remove(enemies, i)
  	end
  end
end

function love.draw(dt)
  -- love.graphics.print("Hello World!", 400, 300)
  love.graphics.draw(player.img,player.x,player.y)
  for i, bullet in ipairs(bullets) do
    love.graphics.draw(bullet.img, bullet.x, bullet.y)
  end

  for i, enemy in ipairs(enemies) do
  	love.graphics.draw(enemy.img, enemy.x, enemy.y)
  end

end

function CheckCollision(x1,y1,w1,h1, x2,y2,w2,h2)
  return x1 < x2+w2 and
         x2 < x1+w1 and
         y1 < y2+h2 and
         y2 < y1+h1
end
