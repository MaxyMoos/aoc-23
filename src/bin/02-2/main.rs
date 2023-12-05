use std::path::Path;


fn main() {
    let input = match std::fs::read_to_string(Path::new("./data/02-1/input.txt")) {
        Ok(input_str) => input_str,
        Err(error) => {
            println!("Error while opening input: {}", error);
            return;
        }
    };

    let mut sum: u32 = 0;

    for (_line_index, line) in input.lines().enumerate() {
        let first: Vec<&str> = line.split(':').collect();
        let sets: Vec<&str> = first[1].trim().split(';').collect();
        let mut min: [u32; 3] = [0, 0, 0];

        for set in sets.iter() {
            let color_data: Vec<&str> = set.split(',').collect();
            for data in color_data.iter() {
                let tmp: Vec<&str> = data.trim().split(' ').collect();
                let qty = tmp[0].parse::<u32>().unwrap();
                let color = tmp[1];
                if color == "red" {
                    if qty > min[0] {
                        min[0] = qty;
                    }
                } else if color == "green" {
                    if qty > min[1] {
                        min[1] = qty;
                    }
                } else if color == "blue" {
                    if qty > min[2] {
                        min[2] = qty;
                    }
                }
            }
        }
        
        sum += min[0] * min[1] * min[2];
    }
    println!("{sum}");
}
