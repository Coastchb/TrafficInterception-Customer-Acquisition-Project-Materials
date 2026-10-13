echo "1) http 首页:"; curl -sI http://neaglegolf.com/ | grep -iE "HTTP/|location"
echo "2) https 首页:"; curl -sI https://neaglegolf.com/ | grep -iE "HTTP/|cf-cache"
echo "3) canonical:"; curl -s https://neaglegolf.com/ | grep -oE '<link rel="canonical"[^>]*>' | head -1
echo "4) robots:"; curl -s https://neaglegolf.com/robots.txt | grep -E "Sitemap|^User-agent"
echo "5) sitemap:"; curl -sI https://neaglegolf.com/sitemap.xml | grep -iE "HTTP/"
echo "6) 不存在路径(应404):"; curl -sI "https://neaglegolf.com/no-such-$(date +%s)/" | grep -iE "HTTP/"
echo "7) www http:"; curl -sI --max-time 10 http://www.neaglegolf.com/ | grep -iE "HTTP/|location"
echo "8) www https:"; curl -sI --max-time 10 https://www.neaglegolf.com/ | grep -iE "HTTP/|location"


curl -sI http://www.neaglegolf.com/
curl -sI https://www.neaglegolf.com/
curl -sI http://www.neaglegolf.com/golf-simulators/
curl -sI https://www.neaglegolf.com/golf-simulators/
