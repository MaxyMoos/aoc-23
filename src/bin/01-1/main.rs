use std::path::Path;

const INTS: [char; 10] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];

fn main() {
    let input = match std::fs::read_to_string(Path::new("./data/01-1/input")) {
        Ok(input_str) => input_str,
        Err(error) => {
            println!("Error while opening input: {}", error);
            return;
        }
    };

    let mut sum: u32 = 0;
    let mut start: char = '\0';
    let mut end: char = '\0';

    for char in input.chars() {
        if char == '\n' {
            if end == '\0' {
                end = start;
            }
            sum += (format!("{}{}", start, end)).parse::<u32>().unwrap();
            start = '\0';
            end = '\0';
        }
        if INTS.contains(&char) {
            if start == '\0' { start = char }
            else { end = char }
        }
    }
    println!("Sum = {}", sum);
}
