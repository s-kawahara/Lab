inputs = readlines
results = Array.new
inputs.each do |input|
  input.chomp!
  input = input.split(" ")
  result = ''
  (0..77).each do |x|
    case x.to_s
    when input[0]
      result << '1'
    when input[1]
      if input[1] == '0'
        result << '0'
      else
        result << '1'
      end
    when input[2]
      result << '1'
    else
      result << '0'
    end
    result << ' '
  end
  results.push(result.rstrip)
end
puts results
