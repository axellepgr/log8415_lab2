import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.*;


public class FriendRecommendation {

    public static class Map extends Mapper<LongWritable, Text, LongWritable, MutualFriendsWritable> {

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            //This section is the processing of one line 
            //In the format: userId friendId1, firendId2, friendsId3 ...
            String line[] = value.toString().split("\t");
            Long curUser = Long.parseLong(line[0]);
            //List of first degree friends of the user
            List<Long> friends = new ArrayList<Long>();
            
            if (line.length > 1 ) {
                StringTokenizer tokenizer = new StringTokenizer(line[1], ",");

                //Go through all the 1st degree friends
                while (tokenizer.hasMoreTokens()) {
                    Long friendDeg1 = Long.parseLong(tokenizer.nextToken());
                    friends.add(friendDeg1);
                    //Add the a relationship between the user and his first degree friend
                    //By witing it to the contex by adding a -1 means they are first degree friends
                    //So that this relationship will not be taken into consideration when chosing mutual friends
                    context.write(new LongWritable(curUser), new MutualFriendsWritable(friendDeg1, -1));
                }

                //For all the friends
                //Create a new pair (friendId1, (friendId2, 1)) 
                for (int i = 0; i < friends.size(); i++) {
                    for (int j = i + 1; j < friends.size(); j++) {
                        context.write(new LongWritable(friends.get(i)), new MutualFriendsWritable((friends.get(j)), 1));
                        context.write(new LongWritable(friends.get(j)), new MutualFriendsWritable((friends.get(i)), 1));
                    }
                }
            }
        }
    }

    //In the map phase we should have something like this:
    //given --> u1 u2, u3
    //1st deg
    //(u1, (u2, -1))
    //(u2, (u3, -1))
    //2nd deg aka possible recommendation
    //(u2, (u3, 1))
    //(u3, (u2, 1))

    public static class Reduce extends Reducer<LongWritable, MutualFriendsWritable, LongWritable, Text> {
        public void reduce(LongWritable key, Iterable<MutualFriendsWritable> values, Context context)
                throws IOException, InterruptedException {

            //For each recommanded friend hold a list of the mutal friends
            //Our goal is to pick the second degree friends with the most mutual friends
            final java.util.Map<Long, Integer> mutualFriends = new HashMap<Long, Integer>();
            //All the writables that share a key
            for (MutualFriendsWritable val : values) {
                final Long toUser = val.user;
                final Integer mutualFriend = val.mutualFriend;

                if (mutualFriends.containsKey(toUser)) {
                    if (mutualFriend == -1) {
                        //We set the count to -1 because they are already friends
                        mutualFriends.put(toUser, -1);
                    } else if (mutualFriends.get(toUser) != -1) { //if it is -1 we don't overide
                        //We append the new recommendation if they are not friends
                        Integer count = mutualFriends.get(toUser);
                        mutualFriends.put(toUser, (count + 1));
                    }
                } else { //If the hash map does not contain the key to that user we add him
                    //We follow the same logic as above
                    if (mutualFriend != -1) {
                        mutualFriends.put(toUser, 1);
                    } else {
                        mutualFriends.put(toUser, -1);
                    }
                }
            }

            //Sorting the friends recommandation based on the number of mutual friends
            SortedMap<Long, Integer> sortedMutualFriends = new TreeMap<Long, Integer>(new Comparator<Long>() {
                public int compare(Long k1, Long k2) {
                    Integer nbrFriends1 = mutualFriends.get(k1);
                    Integer nbrFriends2 = mutualFriends.get(k2);
                    Integer diff = nbrFriends2 - nbrFriends1;
                    //If it has less number of friends it goes lower in the tree
                    //If they have the same number of friends return in ascending order of the id
                    if (diff == 0 && k1 < k2){
                        return -1;
                    }
                    else if (diff < 0){
                        return -1;
                    }
                    return 1;
                }
            });

            for (java.util.Map.Entry<Long, Integer> entry : mutualFriends.entrySet()) {
                if (entry.getValue() != -1) {
                    sortedMutualFriends.put(entry.getKey(), entry.getValue());
                }
            }

            int i = 0;
            String recommandations = "";
            for (java.util.Map.Entry<Long, Integer> entry : sortedMutualFriends.entrySet()) {
                i++;
                if (i == 1) {
                    recommandations = entry.getKey().toString();
                } else {
                    recommandations += "," + entry.getKey().toString();
                }
                if (i == 10){
                    //We only want the 10 first 
                    break;
                }
            }
            context.write(key, new Text(recommandations));
        }
    }

      static public class MutualFriendsWritable implements Writable {
        public Long user;
        public Integer mutualFriend;

        //Creats a new MutualFriendsWritable objects
        //The user id and the list of mutual friends as attributes
        public MutualFriendsWritable(Long user, Integer mutualFriend) {
            this.user = user;
            this.mutualFriend = mutualFriend;
        }
        //-1 will mean no relationship
        public MutualFriendsWritable() {
            this(-1L, -1);
        }

        public void write(DataOutput out) throws IOException {
            out.writeLong(user);
            out.writeInt(mutualFriend);
        }

        public void readFields(DataInput in) throws IOException {
            user = in.readLong();
            mutualFriend = in.readInt();
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();

        Job job = new Job(conf, "FriendRecommendation");
        job.setJarByClass(FriendRecommendation.class);
        job.setOutputKeyClass(LongWritable.class);
        job.setOutputValueClass(MutualFriendsWritable.class);

        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);
        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);
        FileSystem outFs = new Path(args[1]).getFileSystem(conf);
        outFs.delete(new Path(args[1]), true);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        job.waitForCompletion(true);
    }
}
