set types JointControllerState JointTrajectoryControllerState JointState
for type in $types
    for line in (cat topic_type.txt)
        if string match -rq $type'$' "$line"
            set cut_string (string match -r '.*(?=:)' "$line")
            echo \(\"$cut_string\", $type,\)
        end
    end
end

