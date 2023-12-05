use std::path::Path;


const INTS: [char; 10] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
const INTS_AS_CHARS: &[&str] = &["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];


#[derive(Debug)]
struct StringCandidate {
    pub string: String,
    pub index: usize
}


fn main() {
    let input = match std::fs::read_to_string(Path::new("./data/01-1/input")) {
        Ok(input_str) => input_str,
        Err(error) => {
            println!("Error while opening input: {}", error);
            return;
        }
    };

    let mut candidates: Vec<StringCandidate> = vec![];
    let mut to_drop: Vec<usize> = vec![];
    let mut start: char = '\0';
    let mut end: char = '\0';
    let mut sum: u32 = 0;
    let mut clean_before: bool = false;
    let mut clean_after: bool = false;

    for char in input.chars() {
        if char == '\n' {
            if end == '\0' {
                end = start;
            }
            sum += (format!("{}{}", start, end)).parse::<u32>().unwrap();
            start = '\0';
            end = '\0';
            candidates = vec![];
            continue;
        }
        if INTS.contains(&char) {
            if start == '\0' {
                start = char;
                candidates = vec![];
                to_drop = vec![];
            }
            else {
                end = char;
            }
        } else {            
            // check existing candidates
            for (candidate_index, candidate) in candidates.iter_mut().enumerate() {
                if char == candidate.string.chars().nth(candidate.index + 1).unwrap() {
                    candidate.index += 1;
                } else {
                    to_drop.insert(0, candidate_index);
                }
                if candidate.index == candidate.string.len() - 1 {
                    if start == '\0' {
                        start = INTS[INTS_AS_CHARS.iter().position(|&x| x == &candidate.string).unwrap() + 1];
                        clean_after = true;
                    }
                    else {
                        end = INTS[INTS_AS_CHARS.iter().position(|&x| x == &candidate.string).unwrap() + 1];
                        clean_before = true;
                    }
                }
            }

            if clean_before {
                candidates = vec![];
                to_drop = vec![];
                clean_before = false;
            }

            for index in &to_drop {
                candidates.remove(*index);
            }
            to_drop = vec![];
            
            // check if a new candidate pops up
            for candidate in INTS_AS_CHARS.iter() {
                if char == candidate.chars().nth(0).unwrap() {
                    candidates.push(StringCandidate{ string: candidate.to_string(), index: 0 });
                }
            }

            if clean_after {
                candidates = vec![];
                to_drop = vec![];
                clean_after = false;
            }
        }
        
    }
    println!("Sum = {}", sum);
}
