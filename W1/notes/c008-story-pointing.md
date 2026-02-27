# Story Pointing

## Learning Objectives

- Understand what story points are and why they are used
- Learn common estimation techniques for story pointing
- Recognize how story points fit into sprint planning

## Why This Matters

Estimating work is essential for planning sprints and managing stakeholder expectations. Story points provide a relative, team-based approach to estimation that accounts for complexity, uncertainty, and effort. Mastering this skill helps you contribute to effective sprint planning and predictable delivery.

## The Concept

### What Are Story Points?

**Story points** are a unit of measure used in Agile to estimate the effort required to complete a user story or task. Unlike hours or days, story points represent **relative effort** rather than absolute time.

A user story that is twice as complex as another might receive twice as many story points, regardless of how long it actually takes.

### Why Use Story Points Instead of Time?

- **Accounts for complexity:** Not all work is equal; some tasks are harder even if they take similar time
- **Reduces pressure:** Developers are not locked into specific time commitments
- **Encourages team discussion:** Estimation becomes a collaborative exercise
- **Improves over time:** Teams calibrate their velocity based on historical data

### Common Story Point Scales

**Fibonacci Sequence (Most Common):**

```
1, 2, 3, 5, 8, 13, 21, ...
```

The gaps between numbers grow, reflecting increasing uncertainty for larger tasks.

**T-Shirt Sizes:**

```
XS, S, M, L, XL
```

Used for quick, rough estimates before refining.

**Powers of 2:**

```
1, 2, 4, 8, 16
```

Another scale that emphasizes relative sizing.

### Estimation Techniques

#### Planning Poker

1. Each team member has cards with point values (1, 2, 3, 5, 8, 13, etc.)
2. A user story is presented and discussed
3. Everyone selects a card and reveals simultaneously
4. If estimates differ significantly, the team discusses and re-estimates
5. Consensus is reached on the final point value

#### Affinity Estimation

1. Write user stories on cards or sticky notes
2. As a team, sort stories into groups of similar size
3. Assign point values to each group, relative to a reference story

#### Reference Story

1. Identify a well-understood story and assign it a baseline (e.g., 3 points)
2. Estimate other stories relative to this reference
3. "Is this story bigger or smaller than our reference?"

### Factors to Consider When Estimating

- **Complexity:** How difficult is the logic or algorithm?
- **Uncertainty:** How much is unknown or requires research?
- **Effort:** How much work is involved?
- **Risk:** What could go wrong?

### Velocity

**Velocity** is the average number of story points a team completes per sprint. It is used to:

- Plan how much work to commit to in future sprints
- Track team performance over time
- Forecast project completion

Example: If a team completes 25 points per sprint on average, they can plan to take on approximately 25 points of work in the next sprint.

### Common Pitfalls

- **Comparing across teams:** Story points are team-specific; do not compare one team's velocity to another's
- **Inflating estimates:** Be honest; padding leads to inaccurate velocity
- **Ignoring uncertainty:** Large stories should be broken down to reduce risk

## Summary

- Story points measure relative effort, not absolute time
- The Fibonacci sequence is the most common scale
- Techniques like Planning Poker encourage team discussion and consensus
- Velocity helps teams plan sprints and forecast delivery

## Additional Resources

- [Atlassian: Story Points and Estimation](https://www.atlassian.com/agile/project-management/estimation)
- [Mountain Goat Software: Story Points](https://www.mountaingoatsoftware.com/blog/what-are-story-points)
- [Scrum.org: Estimation in Scrum](https://www.scrum.org/resources/blog/practical-fibonacci-beginners-guide-relative-sizing)
