use std::path::Path;


fn main() {
    let input = match std::fs::read_to_string(Path::new("./data/02-1/input.txt")) {
        Ok(input_str) => input_str,
        Err(error) => {
            println!("Error while opening input: {}", error);
            return;
        }
    };

    let mut good_games: u32 = 0;

    for (_line_index, line) in input.lines().enumerate() {
        let mut bad_game: bool = false;
        let first: Vec<&str> = line.split(':').collect();
        let game_id: &str = first[0].split(' ').collect::<Vec<&str>>()[1];
        let sets: Vec<&str> = first[1].trim().split(';').collect();

        for set in sets.iter() {
            let color_data: Vec<&str> = set.split(',').collect();
            for data in color_data.iter() {
                let tmp: Vec<&str> = data.trim().split(' ').collect();
                let qty = tmp[0].parse::<u32>().unwrap();
                let color = tmp[1];
                if color == "red" {
                    if qty > 12 {
                        bad_game = true;
                        break;
                    }
                } else if color == "green" {
                    if qty > 13 {
                        bad_game = true;
                        break;
                    }
                } else if color == "blue" {
                    if qty > 14 {
                        bad_game = true;
                        break;
                    }
                }
            }
            if bad_game { break }
        }
        if !bad_game {
            good_games += game_id.parse::<u32>().unwrap();
        }
    }
    println!("{good_games}");
}
