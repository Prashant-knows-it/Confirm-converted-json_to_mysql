package com.example.Confirm_converted_json_to_mysql;

import java.util.Set;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "movies")
public class Movie {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "movie_id", unique = true)
    private Long movieId;

    private String title;
    private String releaseDate;
    
    @Column(columnDefinition = "TEXT")
    private String overview;

    private String posterPath;
    private Long budget;
    private Long revenue;
    private Float popularity;
    private Float voteAverage;
    private Integer voteCount;

    @ManyToMany
    @JoinTable(
        name = "movie_genres",
        joinColumns = @JoinColumn(name = "movie_id", referencedColumnName = "movie_id"),
        inverseJoinColumns = @JoinColumn(name = "genre_id")
    )
    private Set<Genre> genres;
}
